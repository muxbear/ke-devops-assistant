from langchain_core.messages import AnyMessage
from langgraph.constants import END, START
from langgraph.graph import StateGraph, add_messages
from typing_extensions import TypedDict, Annotated

from agent.llm import dashscope_llm
from agent.util.gitlab_tools import create_gitlab_project
from agent.util.mysql_tools import create_mysql_database

class DevOpsState(TypedDict):
    messages: Annotated[list[AnyMessage], add_messages]
    project_name: str
    project_path: str

def llm_node(state: DevOpsState):
    print('进入节点：llm_node')
    print(f'llm_node state: {state}')

    tools = [create_gitlab_project, create_mysql_database]
    llm_with_tools = dashscope_llm.bind_tools(tools)

    return { "messages": [llm_with_tools.invoke(state['messages'])] }

def routing_func(state: DevOpsState):
    print('进入节点：routing_func')
    print(f'routing_func state: {state}')

    message = state['messages'][-1]
    print(f'message: {message}')

    return END

def tool_node(state: DevOpsState):
    print('进入节点：tool_node')
    print(f'tool_node state: {state}')

    return { "project_path": "test-project" }

agent_builder = StateGraph(DevOpsState)

agent_builder.add_node(llm_node)
agent_builder.add_node(tool_node)

agent_builder.add_edge(START, 'llm_node')
agent_builder.add_conditional_edges('llm_node', routing_func, {"tool_node": "tool_node", END: END})
agent_builder.add_edge('tool_node', 'llm_node')

agent = agent_builder.compile()

response = agent.invoke({"messages": [{"role": "user", "content": "你好"}]})
print(response)
