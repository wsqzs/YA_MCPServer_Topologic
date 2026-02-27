import json
from resources import YA_MCPServer_Resource
from typing import Any

@YA_MCPServer_Resource(
    "resources://project_sop",
    name="project_sop",
    title="项目逻辑建模标准作业流程 (SOP)",
    description="定义了如何从文本中提取任务依赖关系并进行图建模的规范。"
)
def get_project_sop() -> str:
    return """
    # 逻辑建模标准作业程序 (SOP)
    
    1. 依赖识别：
       - 识别文本中的前置任务 (Pre) 和后置任务 (Post)。
       - 逻辑定义：如果任务 B 的启动必须以任务 A 的完成为前提，则 A 是 Pre，B 是 Post。
    
    2. 命名规范：
       - 任务名称应简洁明确。统一使用简体中文。
    
    3. 关系方向：
       - 在图数据库中，关系始终表示为 (Post)-[:DependsOn]->(Pre)。
       - 禁止创建循环依赖。
    """

@YA_MCPServer_Resource(
    "resources://neo4j_schema",
    name="neo4j_schema",
    title="Neo4j 图数据库 Schema 描述",
    description="描述了数据库中 Task 节点和 DependsOn 关系的结构。"
)
def get_neo4j_schema() -> str:
    schema = {
        "node_labels": {"Task": {"properties": ["name"]}},
        "relationship_types": {
            "DependsOn": "从后置任务指向前置任务 (Post)-[:DependsOn]->(Pre)"
        }
    }
    return json.dumps(schema, ensure_ascii=False, indent=2)

@YA_MCPServer_Resource(
    "resources://demo_json",
    name="demo_logic_json",
    title="批量同步示例数据",
    description="提供 batch_upsert_logic 工具的标准输入示例。"
)
def get_demo_json() -> str:
    demo = {
        "example": [
            {"pre": "系统设计", "post": "后端开发"},
            {"pre": "后端开发", "post": "系统联调"}
        ]
    }
    return json.dumps(demo, ensure_ascii=False, indent=2)