# %%
from IPython.display import Image, display
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage
from langgraph.graph import StateGraph, MessagesState, START, END
from langgraph.prebuilt import ToolNode, tools_condition
import os

from dotenv import load_dotenv
load_dotenv()

# 定义工具
def multiply(a: int, b: int) -> int:
    """Multiply a and b.

    Args:
        a: first int
        b: second int
    """
    return a * b

# 初始化模型并绑定工具
llm = ChatOpenAI(
    api_key=os.environ.get("CUSTOM_API_KEY"),
    base_url=os.environ.get("CUSTOM_BASE_URL"),
    model=os.environ.get("CUSTOM_MODEL_NAME") # 确保这里是 deepseek-chat 或相关名称
)
llm_with_tools = llm.bind_tools([multiply])

# 定义节点
def tool_calling_llm(state: MessagesState):
    return {"messages": [llm_with_tools.invoke(state["messages"])]}

# 构建图
builder = StateGraph(MessagesState)
builder.add_node("tool_calling_llm", tool_calling_llm)
builder.add_node("tools", ToolNode([multiply]))
builder.add_edge(START, "tool_calling_llm")
builder.add_conditional_edges("tool_calling_llm", tools_condition)
builder.add_edge("tools", END)
graph = builder.compile()

# 可视化
display(Image(graph.get_graph().draw_mermaid_png()))

# 测试场景 1：工具调用
print("=== 测试 1：工具调用 ===")
result = graph.invoke({"messages": [HumanMessage(content="What is 2 multiplied by 3?")]})
for m in result['messages']:
    m.pretty_print()

# 测试场景 2：直接回答
print("\n=== 测试 2：直接回答 ===")
result = graph.invoke({"messages": [HumanMessage(content="Hello world.")]})
for m in result['messages']:
    m.pretty_print()

# %%