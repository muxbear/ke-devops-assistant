# 智能运维助手 (Ke Operation and Maintenance Assistant)

> 这是一个 DevOps AI 助手智能体，可以协助运维人员进行智能化运维：
> + 在 GitLab 中创建代码仓库
> + 根据初始化脚本创建数据库

## 🌟 核心特性

* ⚡ **高性能异步**：基于 Python 协程（`asyncio`）构建，支持高并发 I/O。
* 🛡️ **强类型约束**：全量使用 Pydantic V2 进行数据验证与类型检查。
* 🧪 **自动化测试**：集成 Pytest 与 Coverage.py，核心逻辑覆盖率 > 90%。
* 🐳 **容器化支持**：多阶段构建的轻量级 Dockerfile。

---

## 🏗 技术栈与架构

### 1. 技术选型

| 模块 | 技术方案                      | 说明 |
| --- |---------------------------| --- |
| **核心框架** | FastAPI                 | 异步高性能 Web 框架 |
| **依赖管理** | uv                      | 现代化的包管理工具 |
| **数据库** | PostgreSQL / Redis        | 关系型与缓存 |
| **ORM** | SQLAlchemy 2.0 / Tortoise | 异步 ORM |
| **后台任务** | Celery / Redis          | 异步任务队列 |

### 2. 项目布局

```text
ke-devops-assistant
├── .python-version    # uv 自动生成的 Python 版本定义
├── pyproject.toml     # 项目元数据与依赖定义
├── uv.lock            # 强一致性依赖锁文件
├── app/               # 源代码核心
│   ├── api/           # 接口路由层
│   ├── core/          # 全局配置、异常、安全设置
│   ├── services/      # 业务逻辑层 (Service Layer)
│   └── models/        # 数据库模型 (SQLAlchemy/Pydantic)
├── tests/             # pytest 测试用例
├── .env.example       # 环境变量示例
└── docker-compose.yml # 本地容器化开发环境

```

---

## 🚀 快速上手

### 前置要求

* **Python**: 3.11+
* **uv**: 1.5.0+ (安装命令：`pip install poetry`)

### 1. 环境安装

```bash
# 克隆项目
git clone https://github.com/your-repo/python-project.git
cd python-project

# 安装 uv
# macOS/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh
# Windows (PowerShell)
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"

```

### 2. 配置环境

```bash
cp .env.example .env
# 编辑 .env 文件，修改数据库地址、API 密钥等

```

### 3. 运行服务

```bash
# 使用 Uvicorn 启动 (FastAPI)
uvicorn app.main:app --reload

```

---

## 🧪 代码质量检查

```bash
# 自动格式化代码
uv run ruff format .

# 静态代码检查与自动修复
uv run ruff check . --fix

```

## 自定化测试
```cmd
# 运行单元测试
uv run pytest tests/
```

---

## 🚢 生产部属

### Dockerfile
见 Dockerfile

```bash
docker-compose up -d
```

---

## 🛠 开发规范

1. **代码风格**：遵循 **PEP 8** 规范，强制使用 `Black` 格式化。
2. **异常处理**：所有业务异常需继承自 `app.core.exceptions.BaseBusinessException`。
3. **文档注释**：公共函数必须包含 **Docstring** (建议 Google Style)。

---

## 📄 许可证

[MIT License](https://www.google.com/search?q=LICENSE)

---

### 💡 规范准则：
1. 类型声明：所有公共函数必须使用 Python Type Hints。
2. 锁文件更新：严禁手动修改 uv.lock，必须通过 uv add 或 uv lock 命令更新。
3. Commit 规范：建议使用 feat:, fix:, refactor: 等前缀。