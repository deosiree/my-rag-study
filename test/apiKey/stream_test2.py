import os
from langchain_openai import ChatOpenAI
from langchain.agents import create_agent
from dotenv import load_dotenv
load_dotenv() # 这一行会把 .env 的值加载到 os.environ

# 1. 初始化你已经在 .env 中配置好的 DeepSeek 模型
llm = ChatOpenAI(
    api_key=os.environ.get("CUSTOM_API_KEY"),
    base_url=os.environ.get("CUSTOM_BASE_URL"),
    model=os.environ.get("CUSTOM_MODEL_NAME") # 确保这里是 deepseek-chat 或相关名称
)

def get_weather(location: str):
    """Call to get the current weather."""
    if location.lower() in ["sf", "san francisco"]:
        return "It's 60 degrees and foggy."
    else:
        return "It's 90 degrees and sunny."

# 2. 将 llm 对象传入 agent
# 注意：这里不再传字符串，而是传 llm 实例
agent = create_agent(
    model=llm,
    tools=[get_weather],
)

# 3. 运行流式输出
for chunk in agent.stream(
    {"messages": [{"role": "user", "content": "what is the weather in sf"}]},
    stream_mode="updates"
):
    print(chunk)
    print("\n")