import os
import sys
import logging
from pathlib import Path
from neo4j import GraphDatabase
from tools import YA_MCPServer_Tool

os.environ["PYTHONIOENCODING"] = "utf-8"
os.environ["PYTHONUTF8"] = "1"

logging.basicConfig(level=logging.INFO, stream=sys.stderr)
logger = logging.getLogger("LogicGuardian")
logger.propagate = False
if not logger.handlers:
    h = logging.StreamHandler(sys.stderr)
    h.setFormatter(logging.Formatter('%(levelname)s: %(message)s'))
    logger.addHandler(h)

class Neo4jClient:
    def __init__(self):
        self.uri = "bolt://127.0.0.1:7687"
        self.user = "neo4j"
        self.password = "12345678"  # 确保这与你的 Neo4j Desktop 密码一致
        self._driver = None

    def get_driver(self):
        if self._driver is None:
            try:
                self._driver = GraphDatabase.driver(self.uri, auth=(self.user, self.password))
                self._driver.verify_connectivity()
                logger.info(f"成功连接至本地 Neo4j")
            except Exception as e:
                logger.error(f"无法连接本地 Neo4j: {str(e)}")
                raise e
        return self._driver

    def check_path(self, start, end):
        driver = self.get_driver()
        with driver.session() as session:
            query = """
            MATCH (a:Task {name: $start}), (b:Task {name: $end})
            MATCH p = shortestPath((a)-[:DependsOn*1..15]->(b))
            RETURN [n in nodes(p) | n.name] as path_list
            """
            result = session.run(query, start=start, end=end)
            record = result.single()
            return record["path_list"] if record else None

client = Neo4jClient()

@YA_MCPServer_Tool(
    name="batch_upsert_logic",
    description="""批量同步逻辑链条。输入格式: [{"pre": "A", "post": "B"}]"""
)
async def batch_upsert_logic(relationships: list) -> dict:
    try:
        driver = client.get_driver()
        with driver.session() as session:
            query = """
            UNWIND $rels AS rel
            MERGE (pre:Task {name: rel.pre})
            MERGE (post:Task {name: rel.post})
            MERGE (post)-[:DependsOn]->(pre)
            """
            session.run(query, rels=relationships)
        return {"status": "SUCCESS", "message": f"已存入 {len(relationships)} 组逻辑。"}
    except Exception as e:
        return {"status": "ERROR", "message": str(e)}

@YA_MCPServer_Tool(
    name="validate_project_logic",
    description="校验任务 A 到 B 是否存在合法的依赖路径。"
)
async def validate_project_logic(current_task: str, target_task: str) -> dict:
    try:
        path = client.check_path(current_task, target_task)
        if path:
            return {"status": "VALID", "chain": " -> ".join(path)}
        return {"status": "INVALID", "message": "逻辑链条不通。"}
    except Exception as e:
        return {"status": "ERROR", "message": str(e)}

@YA_MCPServer_Tool(
    name="query_project_context",
    description="查询任务的上下游关系。"
)
async def query_project_context(task_name: str) -> dict:
    try:
        driver = client.get_driver()
        with driver.session() as session:
            query = """
            MATCH (t:Task {name: $name})
            OPTIONAL MATCH (t)-[:DependsOn]->(pre)
            OPTIONAL MATCH (next)-[:DependsOn]->(t)
            RETURN collect(DISTINCT pre.name) as upstream, collect(DISTINCT next.name) as downstream
            """
            res = session.run(query, name=task_name).single()
            return {
                "task": task_name,
                "pre_tasks": res["upstream"],
                "next_tasks": res["downstream"]
            }
    except Exception as e:
        return {"status": "ERROR", "message": str(e)}