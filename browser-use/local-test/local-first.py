import asyncio
import os
from dotenv import load_dotenv
from browser_use import Agent, Browser
from langchain_openai import ChatOpenAI

load_dotenv()

# 1. 定义一个兼容类，显式允许额外字段
class CompatibleChatOpenAI(ChatOpenAI):
    # 允许 Pydantic 接收初始化之外的属性
    model_config = {"extra": "allow"}

async def main():
    # 2. 使用这个兼容类创建 LLM
    llm = CompatibleChatOpenAI(
        api_key=os.environ.get("CUSTOM_API_KEY"),
        base_url=os.environ.get("CUSTOM_BASE_URL"),
        model=os.environ.get("CUSTOM_MODEL_NAME"),
    )

    # 3. 必须设置这两个属性，否则后面还会报 register_llm 错误
    llm.provider = 'openai'
    llm.model = os.environ.get("CUSTOM_MODEL_NAME")

    # 4. 初始化浏览器
    browser = Browser()

    # 5. 初始化 Agent
    agent = Agent(
        task="去百度搜索 'GitHub'，并告诉我第一个结果的标题是什么",
        llm=llm,
        browser=browser,
    )

    try:
        result = await agent.run()
        print(f"\n任务结果: {result}")
    finally:
        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())