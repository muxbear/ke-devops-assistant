from fastapi import APIRouter
from fastapi.responses import StreamingResponse
import json

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


@graph_router.post("/graph/create_project_stream",
                   summary="流式创建项目",
                   description="流式创建一个项目，包含：1. 创建 gitlab 仓库；2. 创建数据库；返回流式事件")
async def create_project_stream(graph_input_schema: GraphInputSchema):
    print(f"进入流式接口 create_project_stream: {graph_input_schema}")

    config = graph_input_schema.config
    question = graph_input_schema.question

    # 将 config 转换为 deepagents 期望的格式
    if config is not None:
        deepagents_config = {"configurable": config.model_dump()}
    else:
        deepagents_config = {"configurable": {}}

    # 准备输入
    input_data = {"messages": [{"role": "user", "content": question}]}

    async def event_generator():
        """生成流式事件的异步生成器"""
        try:
            # 检查 graph 对象是否支持 astream_events 方法
            if hasattr(graph, 'astream_events'):
                # 使用 astream_events 获取事件流
                async for event in graph.astream_events(input_data, config=deepagents_config, version="v1"):
                    # 将事件转换为 JSON 字符串并发送
                    event_data = json.dumps(event, ensure_ascii=False, default=str)
                    yield f"data: {event_data}\n\n"
            elif hasattr(graph, 'astream'):
                # 回退到 astream 方法
                async for chunk in graph.astream(input_data, config=deepagents_config):
                    # 将块转换为 JSON 字符串并发送
                    chunk_data = json.dumps({"type": "chunk", "data": chunk}, ensure_ascii=False, default=str)
                    yield f"data: {chunk_data}\n\n"
            else:
                # 如果都不支持，返回错误
                error_data = json.dumps({"error": "Graph object does not support streaming", "type": "error"}, ensure_ascii=False)
                yield f"data: {error_data}\n\n"

        except Exception as e:
            error_data = json.dumps({"error": str(e), "type": "error"}, ensure_ascii=False)
            yield f"data: {error_data}\n\n"
        finally:
            # 发送结束标记
            yield "data: [DONE]\n\n"

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no",
        }
    )