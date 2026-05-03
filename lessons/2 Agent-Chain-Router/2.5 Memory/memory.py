# %%
## 完整案例代码
from IPython.display import Image, display
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
from langgraph.graph import START, StateGraph, MessagesState
from langgraph.prebuilt import tools_condition, ToolNode
from langgraph.checkpoint.memory import MemorySaver
import os
from dotenv import load_dotenv

load_dotenv()  # 加载 .env 里的变量
# 1. 定义工具函数
def add(a: int, b: int) -> int:
    """Adds a and b.

    Args:
        a: first int
        b: second int
    """
    return a + b

def multiply(a: int, b: int) -> int:
    """Multiply a and b.

    Args:
        a: first int
        b: second int
    """
    return a * b

def divide(a: int, b: int) -> float:
    """Divide a and b.

    Args:
        a: first int
        b: second int
    """
    return a / b

tools = [add, multiply, divide]

# 2. 初始化模型并绑定工具（需要设置 OPENAI_API_KEY）
llm = ChatOpenAI(
    api_key=os.environ.get("CUSTOM_API_KEY"),
    base_url=os.environ.get("CUSTOM_BASE_URL"),
    model=os.environ.get("CUSTOM_MODEL_NAME"),
)
llm_with_tools = llm.bind_tools(tools)

# 3. 定义系统消息和 assistant 节点
sys_msg = SystemMessage(content="You are a helpful assistant tasked with performing arithmetic on a set of inputs.")

def assistant(state: MessagesState):
    return {"messages": [llm_with_tools.invoke([sys_msg] + state["messages"])]}

# 4. 构建图
builder = StateGraph(MessagesState)
builder.add_node("assistant", assistant)
builder.add_node("tools", ToolNode(tools))
builder.add_edge(START, "assistant")
builder.add_conditional_edges("assistant", tools_condition)
builder.add_edge("tools", "assistant")

# 5. 创建 Memory 并编译图
memory = MemorySaver()
react_graph_memory = builder.compile(checkpointer=memory)

# 可视化
display(Image(react_graph_memory.get_graph().draw_mermaid_png()))

# 6. 测试 Memory 功能
config = {"configurable": {"thread_id": "1"}}

# 第一轮对话
print("=== 第一轮对话 ===")
messages = [HumanMessage(content="Add 3 and 4.")]
result = react_graph_memory.invoke({"messages": messages}, config)
for m in result['messages']:
    m.pretty_print()

# 第二轮对话（同一 thread_id，Memory 生效）
print("\n=== 第二轮对话（Memory 生效）===")
messages = [HumanMessage(content="Multiply that by 2.")]
result = react_graph_memory.invoke({"messages": messages}, config)
for m in result['messages']:
    m.pretty_print()
# %%