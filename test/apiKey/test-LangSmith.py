import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

load_dotenv()  # 加载 .env 里的变量

llm = ChatOpenAI(
    api_key=os.environ.get("CUSTOM_API_KEY"),
    base_url=os.environ.get("CUSTOM_BASE_URL"),
    model=os.environ.get("CUSTOM_MODEL_NAME"),
)
llm.invoke("你好，LangSmith！")  # 这一行会被自动追踪
