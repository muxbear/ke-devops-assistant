"""LangGraph 工作流图定义."""
from langgraph.constants import END, START
from langgraph.graph import StateGraph
from typing_extensions import TypedDict

from agent.util.gitlab_tools import create_gitlab_project_impl
from agent.util.mysql_tools import create_mysql_database_impl

class DevOpsState(TypedDict):
    """DevOps 工作流状态."""
    project_group: str
    project_name: str

    is_gitlab_created: bool
    is_database_created: bool

def create_gitlab_project(state: DevOpsState):
    """在 GitLab 上创建项目."""
    result = create_gitlab_project_impl(state["project_group"], state["project_name"], state["project_name"])
    return result

def create_database(state: DevOpsState):
    """创建项目数据库."""
    # 直接使用项目名称作为数据库名称
    result = create_mysql_database_impl(state["project_name"])
    return result

graph_builder = StateGraph(DevOpsState)

graph_builder.add_node(create_gitlab_project)
graph_builder.add_node(create_database)

graph_builder.add_edge(START, "create_gitlab_project")
graph_builder.add_edge("create_gitlab_project", "create_database")
graph_builder.add_edge("create_database", END)

graph = graph_builder.compile()
