## YA_MCPServer_Template

基于 Neo4j 图数据库的逻辑建模与项目依赖分析助手，旨在通过 MCP 协议将非结构化长文本转化为结构化的任务拓扑图，并提供逻辑合法性校验。

### 组员信息

| 姓名 | 学号 | 分工 | 备注 |
| :--: | :--: | :--: | :--: |
| 万斯球 | U202414885 | MCP Server 开发、Neo4j 建模 | 负责核心逻辑与工具集成 |

### Tool 列表

| 工具名称 | 功能描述 | 输入 | 输出 | 备注 |
| :------: | :------: | :--: | :--: | :--: |
| `batch_upsert_logic` | 批量同步任务逻辑关系到 Neo4j | 关系列表 `relationships` | 存入状态与计数 | 核心写入工具 |
| `validate_project_logic` | 校验两个任务间是否存在合法的依赖链 | `current_task`, `target_task` | 校验状态与路径链条 | 路径探测工具 |
| `query_project_context` | 查询特定任务的直接前置与后置上下文 | `task_name` | 上下游任务列表 | RAG 增强查询 |

### Resource 列表

| 资源名称 | 功能描述 | 输入 | 输出 | 备注 |
| :------: | :------: | :--: | :--: | :--: |
| `project_sop` | 项目逻辑建模的标准操作流程规范 | 无 | 文本说明 | 指引 Agent 建模标准 |

### Prompts 列表

| 指令名称 | 功能描述 | 输入 | 输出 | 备注 |
| :------: | :------: | :--: | :--: | :--: |
| `logic_graph_architect` | 引导模型从长文中提取逻辑链条并同步校验 | `text_content` | 结构化任务路线图 | 包含自动建模流程 |

### 项目结构

- `tools`: 包含 `logic_guardian.py`，实现与 Neo4j 数据库的工具交互逻辑。
- `prompts`: 包含 `planner_prompt.py`，定义 Agent 的三阶段建模角色行为。

### 其他需要说明的情况

- **框架使用**：本项目专注于逻辑拓扑管理与图数据库集成，目前未涉及 PyTorch、Tensorflow 等深度学习框架。
- **环境要求**：需配合本地 **Neo4j Desktop** 运行，创建实例时请确保password正确，默认连接协议为 `bolt://127.0.0.1:7687`。
- **日志**：日志系统重定向至 `sys.stderr`，确保 MCP 标准通信通道（stdout）的纯净。