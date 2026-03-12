import os

from agent.config.base_config import BaseConfig


class DashScopeConfig(BaseConfig):
    base_url: str = os.getenv('DASHSCOPE_BASE_URL')
    api_key: str = os.getenv('DASHSCOPE_API_KEY')