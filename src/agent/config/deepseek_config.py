import os

from agent.config.base_config import BaseConfig


class DeepSeekConfig(BaseConfig):
    base_url: str = os.getenv('DEEPSEEK_BASE_URL')
    api_key: str = os.getenv('DEEPSEEK_API_KEY')