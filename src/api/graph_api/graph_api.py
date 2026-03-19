from fastapi import APIRouter

from agent import graph
from api.graph_api.graph_schema import GraphInputSchema, GraphResponseSchema

graph_router = APIRouter()

@graph_router.post("/graph/create_project",
                   summary="创建项目",
                   description="创建一个项目，包含：1. 创建 gitlab 仓库；2. 创建数据库；",
                   response_model=GraphResponseSchema)
async def create_project(graph_input_schema: GraphInputSchema):
    print(f"进入接口 create_project: {graph_input_schema}")

    config = graph_input_schema.config
    question = graph_input_schema.question

    # 将 config 转换为 deepagents 期望的格式
    if config is not None:
        deepagents_config = {"configurable": config.model_dump()}
    else:
        deepagents_config = {"configurable": {}}

    response = await graph.ainvoke({"messages": [
        {"role": "user", "content": question}
    ]}, config=deepagents_config)

    content = response['messages'][-1].content
    graph_response_schema = GraphResponseSchema(response=content)
    return graph_response_schema