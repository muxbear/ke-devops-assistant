import os

from dotenv import load_dotenv
from langchain_deepseek import ChatDeepSeek
from langchain_openai import ChatOpenAI

load_dotenv(verbose=True)

# DeepSeek 大语言模型
deepseek_llm = ChatDeepSeek(api_key=os.getenv("DEEPSEEK_API_KEY"),
                            model='deepseek-chat')

# 千问 大语言模型
dashscope_llm = ChatOpenAI(base_url=os.getenv("DASHSCOPE_BASE_URL"),
                           api_key=os.getenv("DASHSCOPE_API_KEY"),
                           model='qwen-plus')