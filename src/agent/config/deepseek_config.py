from config.base_config import BaseConfig
import os

class DeepSeekConfig(BaseConfig):
    base_url: str = os.getenv('DEEPSEEK_BASE_URL')
    api_key: str = os.getenv('DEEPSEEK_API_KEY')

if __name__ == '__main__':
    print(DeepSeekConfig.base_url)
    print(DeepSeekConfig.api_key)