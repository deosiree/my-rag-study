import asyncio
import os
from dotenv import load_dotenv
from browser_use import Agent, Browser
from langchain_openai import ChatOpenAI

load_dotenv()

class CompatibleChatOpenAI(ChatOpenAI):
    model_config = {"extra": "allow"}

async def main():
    # 无论用 GPT-4o-mini 还是 DeepSeek，只要是中转或非原厂，
    # 建议都加上这种兼容性配置
    llm = CompatibleChatOpenAI(
        api_key=os.environ.get("GPTMINI_API_KEY"),
        base_url=os.environ.get("GPTMINI_BASE_URL"),
        model=os.environ.get("GPTMINI_MODEL_NAME"),
    )
    llm.provider = 'openai'
    llm.model = os.environ.get("GPTMINI_MODEL_NAME")

    browser = Browser()

    # 任务：Webpack 滚动
    # 增加 explicit 指令强制模型遵循 JSON 格式，这是解决 items 报错的关键
    task = """
    访问 https://webpack.docschina.org/concepts/
    然后执行 scroll_down 动作。
    你不需要阅读内容，只需要滚动到底部即可。
    注意：请确保你的每一个响应都包含有效的 'items' 指令列表。
    """

    agent = Agent(
        task=task,
        llm=llm,
        browser=browser,
        use_vision=False 
    )

    try:
        await agent.run()
    except Exception as e:
        print(f"❌ 运行过程中断: {e}")
    finally:
        # 使用 try 防止 BrowserSession 关闭报错影响结果输出
        try:
            await browser.close()
        except:
            pass

if __name__ == "__main__":
    asyncio.run(main())