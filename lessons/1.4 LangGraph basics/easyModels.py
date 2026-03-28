import os

from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_core.messages import HumanMessage
from langchain_openai import ChatOpenAI

load_dotenv()

models = {
    "DeepSeek-Chat": ChatOpenAI(
        api_key=os.environ.get("CUSTOM_API_KEY"),
        base_url=os.environ.get("CUSTOM_BASE_URL"),
        model=os.environ.get("CUSTOM_MODEL_NAME"),
        temperature=0,
    ),
    "DeepSeek-Reasoner": ChatOpenAI(
        api_key=os.environ.get("CUSTOM_API_KEY"),
        base_url=os.environ.get("CUSTOM_BASE_URL"),
        model=os.environ.get("CUSTOM_MODEL_NAME_2"),
        temperature=0,
    ),
}

question = "解释量子计算"

for name, model in models.items():
    response = model.invoke(question)
    print(f"\n{name} 的回答：")
    print(response.content)
    print(f"Token 使用：{response.response_metadata['token_usage']}")
