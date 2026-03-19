from datetime import datetime
from typing import Union

from openai import BaseModel
from pydantic import Field

class BaseUserSchema(BaseModel):
    id: str = Field(description="用户标识", default=None)
    username: str = Field(description="用户名称", default=None)
    age: float = Field(description="用户年龄", default=None)

class UserSchema(BaseUserSchema):
    create_time: Union[datetime, None] = Field(description="创建时间", default=None)

class CreateOrUpdateUserSchema(UserSchema):
    password: str = Field(description='密码', default=None)
    register_date: Union[datetime, None] = Field(description="注册时间", default=None)
    update_time: Union[datetime, None] = Field(description="更新时间", default=None)