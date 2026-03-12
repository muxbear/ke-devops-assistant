from langgraph.constants import END, START
from langgraph.graph import StateGraph
from typing_extensions import TypedDict


class DevOpsState(TypedDict):
    project_name: str
    project_path: str

def llm_node(state: DevOpsState):
    return { "project_name": "测试项目" }

def tool_node(state: DevOpsState):
    return { "project_path": "test-project" }

def routing_func(state: DevOpsState):
    if state["project_path"] == "test-project":
        return "tool_node"
    return END

agent_builder = StateGraph(DevOpsState)

agent_builder.add_node(llm_node)
agent_builder.add_node(tool_node)

agent_builder.add_edge(START, 'llm_node')
agent_builder.add_conditional_edges('llm_node', routing_func, {"tool_node": "tool_node", END: END})
agent_builder.add_edge('tool_node', 'llm_node')

agent = agent_builder.compile()

