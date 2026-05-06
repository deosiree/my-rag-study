# %%
import os
from langchain_openai import ChatOpenAI
from langgraph.graph import MessagesState
from langgraph.prebuilt import ToolNode, tools_condition
from langgraph.graph import StateGraph, START, END

from dotenv import load_dotenv
load_dotenv()

llm = ChatOpenAI(
    api_key=os.environ.get("CUSTOM_API_KEY"),
    base_url=os.environ.get("CUSTOM_BASE_URL"),
    model=os.environ.get("CUSTOM_MODEL_NAME") # 确保这里是 deepseek-chat 或相关名称
)

def multiply(a: int, b: int) -> int:
    """Multiply a and b.

    这是一个函数的多行文档字符串注释，用于描述函数的功能、参数和返回值。
    Args:
        a: first int  # 这是一个单行注释，说明第一个参数a是一个整数
        b: second int  # 这是一个单行注释，说明第二个参数b是一个整数
    """
    return a * b  # 这是一个单行注释，说明函数返回a和b的乘积

llm_with_tools = llm.bind_tools([multiply])

# 构建核心节点
def tool_calling_llm(state: MessagesState):
    """
    
    这是一个工具调用函数，用于调用大语言模型并处理工具调用。
    参数:
        state (MessagesState): 包含消息状态的字典，其中包含"messages"键，存储了消息列表。
    返回:
        dict: 返回一个字典，其中包含"messages"键，值为调用大语言模型后的消息列表。
    """
    # 调用带有工具功能的大语言模型，传入当前状态中的消息
    # 并将返回的结果包装在字典中返回
    return {"messages": [llm_with_tools.invoke(state["messages"])]}



# 创建工具节点
tool_node = ToolNode([multiply])

# tools_condition 是预构建的条件函数

# 构建图

# 创建图
builder = StateGraph(MessagesState)

# 添加节点
builder.add_node("tool_calling_llm", tool_calling_llm)
builder.add_node("tools", tool_node)

# 添加边
builder.add_edge(START, "tool_calling_llm")

# 添加条件边
builder.add_conditional_edges(
    "tool_calling_llm",
    tools_condition,
)

builder.add_edge("tools", END)

# 编译
graph = builder.compile()

# 🎨 可视化图结构
from IPython.display import Image, display
display(Image(graph.get_graph().draw_mermaid_png()))

# %%