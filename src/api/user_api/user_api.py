from fastapi import APIRouter
from api.user_api.user_schema import UserSchema, CreateOrUpdateUserSchema

user_router = APIRouter()

@user_router.post("/auth", description="返回认证信息")
def auth():
    return {
        "access_token": "accessorising",
        "token_type": "bearer",
    }

@user_router.get("/user/{id}", response_model=UserSchema, summary="根据用户标识查询用户", description="根据用户标识查询用户")
def get_user_by_id(id: str) -> UserSchema:
    user_schema = UserSchema(
        id=id,
        username="mux",
        age=2.5
    )

    return user_schema

@user_router.get("/user/{username}", response_model=UserSchema, summary="根据用户名查询用户", description="根据用户名查询用户")
def get_user_by_name(username: str) -> UserSchema:
    user_schema = UserSchema(
        id = "1000",
        username = username,
        age = 2.5
    )

    return user_schema

@user_router.post("/register", response_model=UserSchema, summary="用户注册", description="用户注册")
def register(body: CreateOrUpdateUserSchema):
    user_schema = UserSchema(
        id="1001",
        username=body.username,
        age=body.age
    )
    return user_schema

