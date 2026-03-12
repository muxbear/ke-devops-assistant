from langchain_core.messages import AnyMessage, ToolMessage
from langgraph.constants import END, START
from langgraph.graph import StateGraph, add_messages
from typing_extensions import TypedDict, Annotated

from agent.llm import dashscope_llm
from agent.util.custom_tools import build_gitlab_repository, build_mysql_db


class DevOpsState(TypedDict):
    messages: Annotated[list[AnyMessage], add_messages]
    project_group: str
    project_path: str
    database_name: str

def llm_node(state: DevOpsState):
    print('进入节点：llm_node')
    print(f'llm_node state: {state}')

    tools = [build_gitlab_repository, build_mysql_db]
    llm_with_tools = dashscope_llm.bind_tools(tools)

    return { "messages": [llm_with_tools.invoke(state['messages'])] }

def routing_func(state: DevOpsState):
    print('进入节点：routing_func')
    print(f'routing_func state: {state}')

    ai_message = state['messages'][-1]
    print(f'ai_message: {ai_message}')

    # 返回的 AIMessage 中 含有 tool_calls 表示有工具调用，路由到 tool_node 节点
    if hasattr(ai_message, "tool_calls") and len(ai_message.tool_calls) > 0:
        return 'tool_node'

    return END

def tool_node(state: DevOpsState):
    print('进入节点：tool_node')
    print(f'tool_node state: {state}')

    ai_message = state['messages'][-1]
    # 要执行的工具
    tool_calls = ai_message.tool_calls

    tool_messages = []
    for tool_call in tool_calls:
        tool_message = None
        if tool_call['name'] == 'build_gitlab_repository':
            tool_message = ToolMessage(content='成功创建仓库', tool_call_id=tool_call['id'])
        elif tool_call['name'] == 'build_mysql_db':
            tool_message = ToolMessage(content='成功创建数据库', tool_call_id=tool_call['id'])
        tool_messages.append(tool_message)

    return { "messages": tool_messages }

agent_builder = StateGraph(DevOpsState)

agent_builder.add_node(llm_node)
agent_builder.add_node(tool_node)

agent_builder.add_edge(START, 'llm_node')
agent_builder.add_conditional_edges('llm_node', routing_func, {"tool_node": "tool_node", END: END})
agent_builder.add_edge('tool_node', 'llm_node')

agent = agent_builder.compile()

# response = agent.invoke({"messages": [{"role": "user", "content": "帮我初始化一个客户为北京市监局的项目 bjsjj-pro"}]})
# print(response)
