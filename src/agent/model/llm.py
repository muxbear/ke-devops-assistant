from langchain_deepseek import ChatDeepSeek

from agent.config.deepseek_config import DeepSeekConfig

# DeepSeek 大语言模型
deepseek_llm = ChatDeepSeek(api_key=DeepSeekConfig.api_key, model='deepseek-chat')

# 千问 大语言模型
# dashscope_llm = ChatOpenAI(base_url=dashscope_config['base_url'],
#                            api_key=dashscope_config['api_key'],
#                            model='qwen-plus')

# 千问 文本向量模型
# dashscope_em = OpenAI(base_url=dashscope_config['base_url'],
#                       api_key=dashscope_config['api_key'])



if __name__ == "__main__":
    # DeepSeek 文本模型测试
    response = deepseek_llm.invoke('你是谁？')

    # DashScope 向量模型测试
    # response = dashscope_em.embeddings.create(
    #     model='text-embedding-v4',
    #     input="文本向量测试"
    # )
    # print(response)

    # texts = [
    #     "人工智能正在改变世界。",
    #     "Python 是一种非常流行的编程语言。",
    #     "今天天气不错。"
    # ]
    # response = dashscope_em.embed_documents(texts)

    print(response)