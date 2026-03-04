from typing import TypedDict

from langgraph.constants import START, END
from langgraph.graph import StateGraph


class DevOpsState(TypedDict):
    project_code: str
    project_name: str
    project_group: str

    is_gitlab_created: bool
    is_database_created: bool

def get_project_info(state: DevOpsState):
    """从项目注册文档中获取项目信息"""
    project_code = state['project_code']
    # 根据 project_code 查询 project_name
    project_name = '这是一个测试项目'

    return {
        'project_code': state['project_code'],
        'project_name': project_name,
    }

def create_gitlab_project(state: DevOpsState):
    """在 GitLab 上创建项目"""
    print("成功创建 gitlab 仓库")
    return {"is_gitlab_created": True}

def create_database(state: DevOpsState):
    """创建项目数据库"""
    print("成功创建 mysql 数据库")
    return {"is_database_created": True}

graph_builder = StateGraph(DevOpsState)

graph_builder.add_node(get_project_info)
graph_builder.add_node(create_gitlab_project)
graph_builder.add_node(create_database)

graph_builder.add_edge(START, "get_project_info")
graph_builder.add_edge("get_project_info", "create_gitlab_project")
graph_builder.add_edge("create_gitlab_project", "create_database")
graph_builder.add_edge("create_database", END)

graph = graph_builder.compile()
