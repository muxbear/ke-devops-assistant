from langchain_deepseek import ChatDeepSeek
from langchain_openai import ChatOpenAI

from agent.config.dashscope_config import DashScopeConfig
from agent.config.deepseek_config import DeepSeekConfig

# DeepSeek 大语言模型
deepseek_llm = ChatDeepSeek(api_key=DeepSeekConfig.api_key,
                            model='deepseek-chat')

# 千问 大语言模型
dashscope_llm = ChatOpenAI(base_url=DashScopeConfig.base_url,
                           api_key=DashScopeConfig.api_key,
                           model='qwen-plus')