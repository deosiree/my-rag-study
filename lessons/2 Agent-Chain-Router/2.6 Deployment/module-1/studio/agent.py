from typing import Annotated
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
import os
from dotenv import load_dotenv

load_dotenv()  # 加载 .env 里的变量


# 定义工具
@tool
def multiply(a: int, b: int) -> int:
    """Multiply two numbers."""
    return a * b


# 定义状态
class State(TypedDict):
    messages: Annotated[list, add_messages]


# 定义节点
def call_model(state: State):
    llm = ChatOpenAI(
        api_key=os.environ.get("CUSTOM_API_KEY"),
        base_url=os.environ.get("CUSTOM_BASE_URL"),
        model=os.environ.get("CUSTOM_MODEL_NAME"),
    )
    llm_with_tools = llm.bind_tools([multiply])
    response = llm_with_tools.invoke(state["messages"])
    return {"messages": [response]}


# 构建图
graph_builder = StateGraph(State)
graph_builder.add_node("agent", call_model)
graph_builder.add_edge(START, "agent")
graph_builder.add_edge("agent", END)
graph = graph_builder.compile()
