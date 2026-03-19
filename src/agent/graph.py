import asyncio

from deepagents import CompiledSubAgent, create_deep_agent
from langchain.agents import create_agent

from agent.llm import deepseek_llm, dashscope_llm, zhipu_llm
from agent.util.gitlab_tools import create_gitlab_project
from agent.util.mysql_tools import create_mysql_database

main_system_prompt = """
# 角色与核心目标
你是主协调智能体，负责高效处理用户请求。你的首要任务是分析用户问题，若其属于预设的专门领域，则分配给相应的子智能体处理;否则，由你亲自处理

# 任务分配规则
请严格依据以下关键词和领域描述，决定是否进行任务分配:
# GitLab 子智能体负责领域
- **负责内容**: 一切与 GitLab 相关的操作，例如：创建 gitlab 仓库；查询 gitlab 仓库；。
- **触发关键词**: 创建 GitLab 仓库、查询 GitLab 仓库

## MySQL 子智能体负责领域
- **负责内容**: 一切与 MySQL 数据库相关的操作。
- **触发关键词**: 创建 MySQL 数据库、查询数据、查询表

# 工作流程
1. **分析请求**: 仔细阅读用户问题，识别其中的核心意图和关键词。
2. **匹配领域**: 将识别出的关键词与上述“负责领域”进行匹配。
    - 如果问题**明确且主要**属于某一个子领域(例如，问题中同时包含“创建 gitlab 仓库")，则毫不犹豫地将任务分配给对应的子智能体
    - 如果问题**同时涉及**两个子领域(例如，“帮我创建一个 GitLab 仓库和 MySQL 数据库”)，这是一个需要协调的复
    - 如果问题**不属于**上述任何子领域，则由你亲自回答。
3. **执行与响应**: 一旦做出分配决定，即调用相应的子智能体，并将其回复完整地呈现给用户。若是你亲自回答，请确保回应清晰、准确、有帮

# 通用行为规范
你的回答应保持专业、友好和乐于助人的态度。
如果无法确定用户意图，或问题模糊，应主动询问澄清。
对于超出你知识范围或工具能力的问题，如实告知，不要编造信息。  
"""

async def create_aiops_graph():
    # GitLab 智能体
    gitlab_agent = create_agent(
        model=deepseek_llm,
        tools=[create_gitlab_project],
        system_prompt="你是一个 GitLab 子智能体，负责执行 GitLab 相关操作，例如：创建 gitlab 仓库"
    )

    gitlab_sub_agent = CompiledSubAgent(name="gitlab_sub_agent", runnable=gitlab_agent, description="负责 GitLab 相关的操作")

    mysql_agent = create_agent(
        model=dashscope_llm,
        tools=[create_mysql_database],
        system_prompt="你是一个 MySQL 子的智能，负责执行 MySQL 相关操作，例如：创建 MySQL 数据库"
    )

    mysql_sub_agent = CompiledSubAgent(name="mysql_sub_agent", runnable=mysql_agent, description="负责 MySQL 数据库相关的操作")

    return create_deep_agent(model=zhipu_llm,
                             subagents=[gitlab_sub_agent, mysql_sub_agent],
                             system_prompt=main_system_prompt)

# 帮我创建一个gitlab仓库，仓库组：测试组，仓库名：test-project，仓库描述：这是一个测试仓库；再创建 MySQL 数据库，数据名：test_project_db
graph = asyncio.run(create_aiops_graph())
