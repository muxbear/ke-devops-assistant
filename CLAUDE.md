# CLAUDE.md

本文档为 Claude Code (claude.ai/code) 在此代码库中工作提供指导。

## 概述

这是一个基于 LangGraph 的 DevOps 助手，可自动完成 GitLab 仓库创建和 MySQL 数据库创建的项目初始化。项目使用两种不同的智能体架构：
1. **简单工作流** (`src/agent/graph.py`): 工具调用的线性序列 (GitLab → MySQL)
2. **LLM驱动智能体** (`src/agent/devops_agent.py`): 使用 LLM 工具调用来动态决定操作

在 `langgraph.json` 中定义的主要入口点是 `devops_agent.py:agent`。

## 常见开发任务

### 环境设置
```bash
# 安装依赖（开发组包含 mypy、ruff）
pip install -e ".[dev]"

# 设置环境变量（复制 .env.sample 到 .env）
cp .env.sample .env
# 编辑 .env 文件，填入你的 GitLab、MySQL 和 LLM API 凭证
```

### 代码检查和格式化
```bash
# 完整代码检查（ruff + mypy）
make lint

# 格式化代码（ruff format + 导入排序）
make format

# 仅检查已更改的文件（与 main 分支差异）
make lint_diff

# 仅类型检查
python -m mypy --strict src/
```

### 测试
```bash
# 运行单元测试（当前暂无测试，但结构已存在）
make test

# 运行特定测试文件（添加测试后可用）
make test TEST_FILE=tests/unit_tests/test_example.py

# 监视模式（需要 ptw）
make test_watch
```

### 运行智能体
```bash
# 启动 LangGraph 开发服务器
langgraph dev

# API 将可在 http://127.0.0.1:2024 访问
# Studio UI：https://smith.langchain.com/studio/?baseUrl=http://127.0.0.1:2024
```

## 架构

### 状态定义
- `DevOpsState` (位于 `graph.py`): 简单的 TypedDict，包含 `project_group`、`project_name` 和布尔标志
- `DevOpsState` (位于 `devops_agent.py`): 包含 LLM 对话的 `messages` 列表，使用 `add_messages` reducer
- `AiOpsState` (位于 `aiops_agent.py`): 更复杂的状态，带有用于多智能体路由的对话栈，使用自定义的 `update_dialog_stack` reducer

### 归约器 (Reducers)
- `add_messages`: 内置的 LangGraph reducer，将新消息追加到 `messages` 列表
- `update_dialog_stack`: `aiops_agent.py` 中的自定义 reducer，管理智能体状态栈 (`main_agent`、`doc_agent` 等)

### 图模式
- **简单工作流**: 工具节点之间的线性边 (START → create_gitlab_project → create_database → END)
- **LLM驱动**: 基于工具调用的条件路由 (llm_node → routing_func → tool_node 或 END)

### LLM 配置
- **DeepSeek**: 通过 `DEEPSEEK_API_KEY` 和 `DEEPSEEK_BASE_URL` 环境变量配置
- **Qwen (DashScope)**: 通过 `DASHSCOPE_API_KEY` 和 `DASHSCOPE_BASE_URL` 环境变量配置
- LLM 实例在 `src/agent/llm.py` 中创建，并在其他地方导入使用

### 工具定义
工具定义在 `src/agent/util/` 目录中：
- `gitlab_tools.py`: 实际的 GitLab API 实现，包含中文名称的路径清理功能
- `mysql_tools.py`: MySQL 数据库创建，包含名称验证和 utf8mb4 字符集
- `custom_tools.py`: 用于 LLM 测试的桩工具（仅打印语句）

**注意**: `devops_agent.py` 使用 `custom_tools.py` 桩工具，而简单工作流 (`graph.py`) 使用真实实现。工具函数遵循 `@tool` 装饰器模式，并返回包含成功标志的字典。

### 人机协同模式
`devops_agent.py` 使用 `langgraph.types.interrupt` 在执行操作前暂停并请求人工批准（例如 GitLab 仓库创建）。这提供了安全性，但在开发过程中需要手动交互。

### 配置类
配置通过环境变量和 `src/agent/config/` 中的类管理：
- `gitlab_config.py`: 包含 `url` 和 `token` 的 `GitLabConfig`
- `mysql_config.py`: 类似的 MySQL 凭证模式

## 文件结构

```
src/agent/
├── __init__.py
├── graph.py              # 简单线性工作流
├── devops_agent.py       # LLM驱动智能体（主要入口点）
├── aiops_agent.py        # AIOps智能体，带对话栈
├── llm.py                # LLM客户端配置
├── config/               # 配置类
│   ├── __init__.py
│   ├── gitlab_config.py
│   └── mysql_config.py
└── util/                 # 工具实现
    ├── __init__.py
    ├── gitlab_tools.py   # 真实的GitLab API调用
    ├── mysql_tools.py    # 真实的MySQL操作
    └── custom_tools.py   # 用于LLM测试的桩工具
```

## 环境变量

必需的变量（参见 `.env.sample`）：
- `DEEPSEEK_API_KEY`, `DEEPSEEK_BASE_URL` (可选)
- `DASHSCOPE_API_KEY`, `DASHSCOPE_BASE_URL` (可选)
- `gitlab_url`, `gitlab_token`
- `mysql_url`, `mysql_username`, `mysql_password`
- `PYTHONIOENCODING=utf-8`, `PYTHONUTF8=1` (用于 Windows 兼容性)

## 开发注意事项

- 项目使用 **ruff** 进行代码检查和格式化，遵循 Google 风格的文档字符串
- 强制执行 **mypy** 严格模式
- **LangGraph CLI** (`langgraph dev`) 是主要的开发服务器
- 两种智能体风格并存；LLM驱动开发时关注 `devops_agent.py`
- 工具实现分为真实 API 工具 (`gitlab_tools.py`, `mysql_tools.py`) 和用于测试的桩工具 (`custom_tools.py`)
- Windows 用户必须设置 UTF-8 环境变量以处理中文项目名称
- `devops_agent.py` 使用 `interrupt` 实现人机协同批准，在调用工具时会暂停执行并等待用户输入 (`y`/`n`)

## 添加新工具

1. 在 `src/agent/util/` 中实现工具函数（使用 `@tool` 装饰器）
2. 在相关的智能体文件中导入工具
3. 添加到 `llm_node` 的 `tools` 列表（对于 LLM 驱动智能体）或作为新节点（对于简单工作流）
4. 如果需要新字段，更新状态定义

## 以编程方式运行智能体

```python
from agent.devops_agent import agent, DevOpsState

config = {"configurable": {"thread_id": "test_1"}}
response = agent.invoke(
    {"messages": [{"role": "user", "content": "帮我初始化项目..."}]},
    config=config,
)
```