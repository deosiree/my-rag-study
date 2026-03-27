import getpass
import os

# 人类交互获得api key
# def _set_env(var: str):
#     if not os.environ.get(var):
#         os.environ[var] = getpass.getpass(f"{var}: ")

# _set_env("OPENAI_API_KEY")
# _set_env("TAVILY_API_KEY")  # 注册：https://tavily.com
from dotenv import load_dotenv

load_dotenv()  # 这一行会把 .env 的值加载到 os.environ

from langchain_openai import ChatOpenAI
from langchain_community.tools.tavily_search import TavilySearchResults
from langgraph.graph import StateGraph, MessagesState, START, END
from langgraph.prebuilt import ToolNode

# 初始化工具
search = TavilySearchResults(max_results=2)
tools = [search]

# 定义 Agent（添加 ReAct 系统提示词）
llm = ChatOpenAI(
    api_key=os.environ.get("CUSTOM_API_KEY"),
    base_url=os.environ.get("CUSTOM_BASE_URL"),
    model=os.environ.get("CUSTOM_MODEL_NAME"),
)
llm_with_tools = llm.bind_tools(tools)

def agent(state: MessagesState):
    # 添加 ReAct 提示词
    system_message = """你是一个 ReAct (Reasoning + Acting) Agent。
处理用户问题时，请遵循以下步骤：
1. Thought（思考）：分析问题需要什么信息
2. Action（行动）：决定调用哪个工具
3. Observation（观察）：分析工具返回的结果
4. Answer（回答）：基于观察给出最终答案

始终展示你的推理过程。"""

    messages = [{"role": "system", "content": system_message}] + state["messages"]
    return {"messages": [llm_with_tools.invoke(messages)]}

def should_continue(state: MessagesState):
    last_message = state["messages"][-1]
    if hasattr(last_message, "tool_calls") and last_message.tool_calls:
        return "tools"
    return END

# 构建图
graph = StateGraph(MessagesState)
graph.add_node("agent", agent)
graph.add_node("tools", ToolNode(tools))

graph.add_edge(START, "agent")
graph.add_conditional_edges("agent", should_continue, ["tools", END])
graph.add_edge("tools", "agent")

app = graph.compile()

# 测试
response = app.invoke({
    "messages": [("user", "2024年诺贝尔物理学奖获得者是谁？他们的主要贡献是什么？")]
})
print(response["messages"][-1].content)