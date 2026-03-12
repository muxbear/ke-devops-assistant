from langchain_core.messages import AnyMessage
from langgraph.constants import END, START
from langgraph.graph import StateGraph, add_messages
from typing_extensions import TypedDict, Annotated


class DevOpsState(TypedDict):
    messages: Annotated[list[AnyMessage], add_messages]
    project_name: str
    project_path: str

def llm_node(state: DevOpsState):
    print('进入节点：llm_node')
    print(state)

    return { "project_name": "测试项目" }

def routing_func(state: DevOpsState):
    print('进入节点：routing_func')
    print(state)

    return END

def tool_node(state: DevOpsState):
    print('进入节点：tool_node')
    print(state)

    return { "project_path": "test-project" }

agent_builder = StateGraph(DevOpsState)

agent_builder.add_node(llm_node)
agent_builder.add_node(tool_node)

agent_builder.add_edge(START, 'llm_node')
agent_builder.add_conditional_edges('llm_node', routing_func, {"tool_node": "tool_node", END: END})
agent_builder.add_edge('tool_node', 'llm_node')

agent = agent_builder.compile()

