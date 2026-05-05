## 完整案例代码
# from IPython.display import Image, display
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
from langgraph.graph import START, StateGraph, MessagesState
from langgraph.prebuilt import tools_condition, ToolNode
import os
from dotenv import load_dotenv

load_dotenv()  # 加载 .env 里的变量

# 1. 定义工具函数
def multiply(a: int, b: int) -> int:
    """Multiply a and b.

    Args:
        a: first int
        b: second int
    """
    return a * b

def add(a: int, b: int) -> int:
    """Adds a and b.

    Args:
        a: first int
        b: second int
    """
    return a + b

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
llm_with_tools = llm.bind_tools(tools, parallel_tool_calls=False)

# 3. 定义系统消息
sys_msg = SystemMessage(content="You are a helpful assistant tasked with performing arithmetic on a set of inputs.")

# 4. 定义 assistant 节点
def assistant(state: MessagesState):
    return {"messages": [llm_with_tools.invoke([sys_msg] + state["messages"])]}

# 5. 构建图
builder = StateGraph(MessagesState)
builder.add_node("assistant", assistant)
builder.add_node("tools", ToolNode(tools))
builder.add_edge(START, "assistant")
builder.add_conditional_edges("assistant", tools_condition)
builder.add_edge("tools", "assistant")
react_graph = builder.compile()

# # 6. 可视化
# display(Image(react_graph.get_graph().draw_mermaid_png()))

# 7. 测试执行
print("=== 测试：多步数学计算 ===")
messages = [HumanMessage(content="Add 3 and 4. Multiply the output by 2. Divide the output by 5")]
result = react_graph.invoke({"messages": messages})

for m in result['messages']:
    m.pretty_print()