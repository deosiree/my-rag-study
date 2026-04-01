import os

from dotenv import load_dotenv
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_openai import ChatOpenAI

load_dotenv()

chat = ChatOpenAI(
    api_key=os.environ.get("CUSTOM_API_KEY"),
    base_url=os.environ.get("CUSTOM_BASE_URL"),
    model=os.environ.get("CUSTOM_MODEL_NAME"),
    temperature=0,
)
search = TavilySearchResults(max_results=3)


def search_qa(question):
    # 1. 搜索相关信息
    search_results = search.invoke(question)
    context = "\n\n".join([doc["content"] for doc in search_results])

    # 2. 结合搜索结果生成答案
    prompt = f"""基于以下信息回答问题：
                信息：
                {context}
                问题：{question}
                答案：
                """
    print(prompt)
    response = chat.invoke(prompt)
    return response.content


# 使用
answer = search_qa("LangGraph 的主要优势是什么？")
print(answer)
