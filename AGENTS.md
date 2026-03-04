# Agent Development Guide

This document provides guidelines for agents working on this codebase.

## Project Overview

This is a LangGraph-based DevOps assistant project that uses:
- **LangGraph** for agent graph orchestration
- **LangChain** with DeepSeek/Qwen models for LLM interactions
- **Python 3.10+** as the runtime

## Build, Lint, and Test Commands

### Running Tests

```bash
# Run all unit tests
make test
# or
python -m pytest tests/unit_tests/

# Run a specific test file
make test TEST_FILE=tests/unit_tests/test_example.py
# or
python -m pytest tests/unit_tests/test_example.py

# Run tests in watch mode (requires ptw)
make test_watch

# Run integration tests
make integration_tests

# Run with profiling
make test_profile
```

### Linting and Formatting

```bash
# Run full linting (ruff + mypy)
make lint

# Run formatters only
make format

# Lint with diff (only check changed files)
make lint_diff

# Lint specific package
make lint_package

# Lint test files only
make lint_tests
```

### Direct Commands

```bash
# Ruff linting
python -m ruff check .

# Ruff formatting
ruff format .

# Import sorting
ruff check --select I --fix .

# Type checking
python -m mypy --strict src/
```

## Code Style Guidelines

### General Principles

- Use **Python 3.10+** features (use `from __future__ import annotations` where helpful)
- Follow **Google-style** docstrings (enforced by ruff)
- Use **type hints** everywhere (strict mypy)
- Keep functions small and focused

### Imports

- Use **absolute imports** from the package: `from agent.config import ...`
- Group imports in this order: standard library, third-party, local
- Use `isort` for automatic sorting (run `ruff check --select I --fix`)
- Avoid wildcard imports (`from x import *`)

### Naming Conventions

| Element | Convention | Example |
|---------|------------|---------|
| Modules | snake_case | `gitlab_tools.py` |
| Classes | PascalCase | `DevOpsState` |
| Functions | snake_case | `create_gitlab_project` |
| Variables | snake_case | `project_code` |
| Constants | SCREAMING_SNAKE_CASE | `MAX_RETRIES` |
| Type aliases | PascalCase | `DevOpsState` |

### Type Hints

- Always use **explicit type hints** for function parameters and return values
- Use `TypedDict` for structured state dictionaries
- Use `Optional[X]` instead of `X | None`
- Use `Sequence[T]`, `Mapping[K, V]` for generic collections when appropriate

```python
# Good
def create_gitlab_project(state: DevOpsState) -> dict[str, bool]:
    ...

# Avoid
def create_gitlab_project(state):
    ...
```

### Error Handling

- Use **specific exception types**
- Include meaningful error messages
- Handle exceptions at the appropriate level
- Use `logging` instead of `print` for production code

```python
# Good
import logging

logger = logging.getLogger(__name__)

try:
    result = api_call()
except ValueError as e:
    logger.error(f"Invalid input: {e}")
    raise
```

### Docstrings

Follow **Google style** with `Args`, `Returns`, `Raises` sections:

```python
def create_gitlab_project(state: DevOpsState) -> dict[str, bool]:
    """在 GitLab 上创建项目.
    
    Args:
        state: 当前的项目状态,包含项目代码、名称等信息
        
    Returns:
        更新后的状态字典,包含 is_gitlab_created 标志
        
    Raises:
        GitLabAPIError: 当 GitLab API 调用失败时
    """
```

### Project Structure

```
src/agent/
├── __init__.py          # Package exports
├── graph.py             # LangGraph state graph definition
├── config/              # Configuration classes
│   ├── __init__.py
│   ├── base_config.py
│   └── deepseek_config.py
├── model/               # LLM model definitions
│   ├── __init__.py
│   └── llm.py
└── util/                # Utility functions
    ├── __init__.py
    └── gitlab_tools.py
```

### Configuration

- Store configuration in `src/agent/config/`
- Use environment variables for sensitive data
- Create base config classes for extensibility

```python
# Good pattern
from agent.config.deepseek_config import DeepSeekConfig

llm = ChatDeepSeek(
    base_url=DeepSeekConfig.base_url,
    api_key=DeepSeekConfig.api_key,
)
```

### LangGraph Patterns

- Define state as a `TypedDict`
- Use `StateGraph` for workflow definition
- Add nodes with descriptive names
- Define edges explicitly between nodes

```python
class DevOpsState(TypedDict):
    project_code: str
    is_gitlab_created: bool

graph_builder = StateGraph(DevOpsState)
graph_builder.add_node("create_gitlab", create_gitlab_project)
graph_builder.add_edge(START, "create_gitlab")
```

## Testing Guidelines

- Place tests in `tests/` directory
- Use `pytest` as the test framework
- Follow naming convention: `test_*.py`
- Use descriptive test names that explain what is being tested

```python
# Example test structure (when tests are added)
def test_create_gitlab_project_success():
    """测试成功创建 GitLab 项目的场景"""
    state = DevOpsState(
        project_code="test-project",
        project_name="Test Project",
        project_group="mygroup",
        is_gitlab_created=False,
        is_database_created=False,
    )
    result = create_gitlab_project(state)
    assert result["is_gitlab_created"] is True
```

## Dependencies

Install dependencies using:

```bash
# Development dependencies
pip install -e ".[dev]"

# Or use the dev dependency group
pip install -e .
```

Required tools (defined in `pyproject.toml`):
- `ruff` - Linting and formatting
- `mypy` - Type checking
- `pytest` - Testing

## Environment Variables

Create a `.env` file with required variables:

```
DEEPSEEK_BASE_URL=...
DEEPSEEK_API_KEY=...
```

## Running the Agent

```bash
# Using langgraph-cli
npx langgraph dev

# Or run directly
python -m agent.model.llm
```
