import uvicorn
from fastapi import FastAPI, APIRouter

from api.graph_api.graph_api import graph_router
from api.user_api.user_api import user_router

class AiOpsServer:
    def __init__(self):
        self.app = FastAPI(title="AI Ops 服务")

        # 把项目下的 static 目录做为静态文件访问目录（有报错）
        # self.app.mount("../static", StaticFiles(directory="static"), name="static")

        # 创建自定义实例 oauth2
        # my_oauth2 = MyOAuth2PasswordBearer(tokenUrl="/api/token", scheme="Bearer")

    def init_app(self):
        # 初始化全局异常处理
        #TODO

        # 初始化全局中间件
        # TODO

        # 初始化全局 CORS
        # TODO

        # 初始化路由
        self.__init_routers()

    def __init_routers(self):
        root_router = APIRouter()
        root_router.include_router(user_router, tags=["用户服务"])
        root_router.include_router(graph_router, tags=["AI Ops 服务"])
        self.app.include_router(root_router, prefix="/api")

    def run(self, host: str, port: int):
        self.init_app()
        uvicorn.run(self.app, host=host, port=port)


if __name__ == "__main__":
    aiops_server = AiOpsServer()
    aiops_server.run("127.0.0.1", 8000)
