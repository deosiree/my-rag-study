from browser_use import Agent, ChatOpenAI
from dotenv import load_dotenv
import asyncio
import os

load_dotenv()


async def main():
    llm = ChatOpenAI(
        api_key=os.environ.get("GPT_API_KEY"),
        base_url=os.environ.get("GPT_BASE_URL"),
        model=os.environ.get("GPT_MODEL_NAME"),
    )
    task = "在百度搜索框输入 'GitHub'，然后点击 '百度一下' 按钮，最后告诉我搜索结果的第一条标题"
    agent = Agent(task=task, llm=llm)
    await agent.run()


if __name__ == "__main__":
    asyncio.run(main())
