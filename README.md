# DevOps Assistant

基于 LangGraph 的智能 DevOps 助手，集成了 GitLab 仓库创建和 MySQL 数据库创建功能，为项目初始化提供一站式解决方案。

## 功能特性

- 🏗️ **GitLab 仓库创建**：自动创建 GitLab 项目组和仓库
- 🗄️ **MySQL 数据库创建**：自动创建 MySQL 数据库，支持 utf8mb4 字符集
- 🔄 **工作流编排**：使用 LangGraph 实现 DevOps 工作流自动化
- 🌐 **Web 服务**：提供 RESTful API 和 Web UI 交互界面
- 🛡️ **安全命名**：自动处理中文项目名称，转换为有效的 GitLab 路径和数据库名

## 系统要求

- Python 3.10+
- GitLab 8.0+
- MySQL 8.0+

## 快速开始

### 1. 安装依赖

```bash
pip install -e .
```

### 2. 环境配置

创建 `.env` 文件并配置必要的环境变量：

```env
# LangSmith 配置
LANGSMITH_PROJECT=ke-devops-assistant
LANGSMITH_API_KEY=your_langsmith_api_key

# LLM 配置
DEEPSEEK_BASE_URL=https://api.deepseek.com
DEEPSEEK_API_KEY=your_deepseek_api_key

# GitLab 配置
gitlab_url=http://your-gitlab-server:port/
gitlab_token=your_gitlab_access_token

# MySQL 配置
mysql_url=your-mysql-server:port
mysql_username=root
mysql_password=your_mysql_password

# 强制 Python 使用 UTF-8 编码
PYTHONIOENCODING=utf-8
PYTHONUTF8=1
```

### 3. 启动服务

```bash
langgraph dev
```

服务启动后，您可以访问：

- **API 服务**：http://127.0.0.1:2024
- **Studio UI**：https://smith.langchain.com/studio/?baseUrl=http://127.0.0.1:2024
- **API 文档**：http://127.0.0.1:2024/docs

## 使用方法

### 通过 Web UI 使用

1. 打开 Studio UI：https://smith.langchain.com/studio/?baseUrl=http://127.0.0.1:2024
2. 输入以下参数：
   - `project_group`: 项目组名称
   - `project_name`: 项目名称
3. 点击运行，系统将自动：
   - 在 GitLab 上创建项目组和仓库
   - 在 MySQL 上创建数据库

### 通过 API 使用

发送 POST 请求到 `http://127.0.0.1:2024/runs`：

```json
{
  "values": {
    "project_group": "example-group",
    "project_name": "example-project"
  }
}
```

### 命令行测试

您可以使用以下 Python 代码进行测试：

```python
from agent.graph import graph, DevOpsState

# 创建测试状态
state = DevOpsState(
    project_group="测试组",
    project_name="测试项目",
    is_gitlab_created=False,
    is_database_created=False
)

# 运行工作流
result = graph.invoke(state)
print(result)
```

## 项目结构

```
ke-devops-assistant/
├── src/
│   └── agent/
│       ├── __init__.py
│       ├── graph.py              # LangGraph 工作流定义
│       ├── config/
│       │   ├── __init__.py
│       │   ├── gitlab_config.py   # GitLab 配置
│       │   └── mysql_config.py    # MySQL 配置
│       ├── model/
│       │   ├── __init__.py
│       │   └── llm.py            # LLM 模型配置
│       └── util/
│           ├── __init__.py
│           ├── gitlab_tools.py    # GitLab 工具函数
│           └── mysql_tools.py     # MySQL 工具函数
├── pyproject.toml
├── .env                         # 环境变量配置
└── README.md                    # 项目文档
```

## 工作流程

1. **输入参数**：接收项目组名称和项目名称
2. **创建 GitLab 仓库**：
   - 验证和规范化项目组名称
   - 创建或获取项目组
   - 在项目组下创建项目仓库
3. **创建 MySQL 数据库**：
   - 验证和规范化项目名称
   - 创建数据库（使用 utf8mb4 字符集）
   - 返回创建结果
4. **返回结果**：包含 GitLab 和 MySQL 创建状态的信息

## 配置说明

### GitLab 配置

- `gitlab_url`: GitLab 服务器地址
- `gitlab_token`: GitLab 个人访问令牌（需要 api、write_repository 权限）

### MySQL 配置

- `mysql_url`: MySQL 服务器地址
- `mysql_username`: MySQL 用户名（需要有创建数据库的权限）
- `mysql_password`: MySQL 密码

## 命名规则

### GitLab 路径命名

- 支持中文名称，自动转换为有效的 GitLab 路径
- 示例：`测试项目` → `ceshi_xiangmu` 或 `test_project`
- 只包含小写字母、数字、下划线和连字符

### MySQL 数据库名称

- 支持中文名称，自动转换为有效的数据库名称
- 示例：`测试项目` → `ceshi_xiangmu` 或 `test_project`
- 只包含小写字母、数字和下划线
- 不以数字开头

## 故障排除

### 编码问题

如果遇到编码相关的错误，请确保：

1. `.env` 文件使用 UTF-8 编码保存（无 BOM）
2. 设置了正确的环境变量：
   ```bash
   PYTHONIOENCODING=utf-8
   PYTHONUTF8=1
   ```

### 权限问题

1. **GitLab 令牌权限**：确保令牌有 `api` 和 `write_repository` 权限
2. **MySQL 用户权限**：确保用户有创建数据库的权限

### 连接问题

1. 检查 GitLab 和 MySQL 服务器地址是否正确
2. 确保网络连接正常
3. 验证防火墙设置

## 开发说明

### 添加新的工具

1. 在 `src/agent/util/` 目录下创建新的工具文件
2. 实现工具函数，使用 `@tool` 装饰器
3. 在 `src/agent/graph.py` 中集成新工具到工作流

### 扩展工作流

1. 修改 `DevOpsState` 类型定义，添加新的状态字段
2. 创建新的工作流节点函数
3. 在 `graph_builder` 中添加新的节点和边

## 许可证

本项目采用 MIT 许可证。详见 [LICENSE](LICENSE) 文件。

## 贡献

欢迎提交 Issue 和 Pull Request！

## 更新日志

### v0.0.1 (2026-03-04)

- 初始版本发布
- 集成 GitLab 仓库创建功能
- 集成 MySQL 数据库创建功能
- 实现 LangGraph 工作流编排
- 解决 Windows 环境下的编码问题