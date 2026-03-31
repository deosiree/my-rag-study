'''
Author: Spindrift 1692592987@qq.com
Date: 2026-03-31 23:18:10
LastEditors: Spindrift 1692592987@qq.com
LastEditTime: 2026-03-31 23:25:58
FilePath: \my-rag-study\lessons\1.8 Conclusion\customer-service-agent\src\graph\builder.py
Description: LangGraph 枢纽：建图、连边
    1. 定义节点：每个节点是一个函数，输入是 state，输出是 state；
    2. 定义边：每个边是一个函数，输入是 state，输出是 state；
    3. 定义图：图是节点和边的集合；
    4. 定义图的执行：图的执行是图的节点和边的执行；
    5. 定义图的执行结果：图的执行结果是图的节点和边的执行结果；
    6. 定义图的执行结果的输出：图的执行结果的输出是图的节点和边的执行结果的输出；
'''
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
