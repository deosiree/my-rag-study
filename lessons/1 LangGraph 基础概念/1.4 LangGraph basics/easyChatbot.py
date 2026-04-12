import os

from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_core.messages import HumanMessage
from langchain_openai import ChatOpenAI

load_dotenv()

# LangChain 1.2+：用 create_agent（chat 模型必须用 LangChain 的 Chat 模型，不能传 openai.OpenAI）
llm = ChatOpenAI(
    api_key=os.environ.get("CUSTOM_API_KEY"),
    base_url=os.environ.get("CUSTOM_BASE_URL"),
    model=os.environ.get("CUSTOM_MODEL_NAME"),
    temperature=0.7,
)

chat = create_agent(
    llm,
    tools=[TavilySearchResults()],
    system_prompt="你是一个聊天助手，总是能通过web search获取最佳实践，给出2-3个方案，再根据用户输入回答问题。",
)

# 对话历史
history = []


def chat_bot(user_input):
    history.append(HumanMessage(content=user_input))

    result = chat.invoke({"messages": history})

    new_messages = result["messages"]
    # history.clear()# 清空历史
    history.extend(new_messages)#添加新的消息

    last = new_messages[-1]#获取最后一条消息
    return getattr(last, "content", str(last))


# 使用
while True:
    user_input = input("输入Q/q退出，输入其他内容继续: ")
    if user_input.lower() in ["q", "Q"]:
        break
    response = chat_bot(user_input)
    print(f"Bot: {response}")
