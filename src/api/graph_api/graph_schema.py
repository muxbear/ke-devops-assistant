import uuid
from typing import Union

from pydantic import BaseModel, Field

class GraphConfigurableSchema(BaseModel):
    thread_id: Union[str, None] = Field(description="会话标识", default=str(uuid.uuid4()))
    user_id: str = Field(description="用户标识", default=None)

class GraphConfigSchema(BaseModel):
    configurable: Union[GraphConfigurableSchema, None] = Field(description="图的 configurable", default=None)

class GraphInputSchema(BaseModel):
    config: Union[GraphConfigurableSchema, None] = Field(description="图的 config", default=None)
    question: str = Field(description="用户的问题", default=None)

class GraphResponseSchema(BaseModel):
    response: str = Field(description="图的响应", default=None)