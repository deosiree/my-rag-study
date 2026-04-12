"""
Author: Spindrift 1692592987@qq.com
Date: 2026-04-12 20:46:37
LastEditors: Spindrift 1692592987@qq.com
LastEditTime: 2026-04-12 22:37:28
FilePath: \my-rag-study\lessons\2 Agent-Chain-Router\2.0 Introduction\clientServer.py
Description: LangGraph 示例 — 用 LLM 做意图分类，再按 intent 路由到不同节点（无大模型时可将 classify 换成规则函数）。
"""

# %%
# 🎨 可视化图结构
from IPython.display import Image, display
import os
from typing import Annotated, Literal, Optional, TypedDict

from dotenv import load_dotenv
from langchain_core.messages import AIMessage, BaseMessage, HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI
from langgraph.graph import END, START, StateGraph, add_messages
from pydantic import Field, BaseModel
from ipython import visualize_graph

load_dotenv()

# ---------------------------------------------------------------------------
# 1. 状态：图里流转的唯一数据结构（节点返回值会 merge 进这里）
# ---------------------------------------------------------------------------
Intent = Literal["faq", "technical", "complaint"]
TechLev = Literal["high", "low"]


class State(TypedDict):
    messages: Annotated[list, add_messages]  # 追加更新
    intent: Optional[Intent]
    tech_lev: Optional[TechLev]


# ---------------------------------------------------------------------------
# 2. 图式：图里流转的路径。它不仅是定义数据结构的工具，更是系统各组件之间沟通的“协议”。
#  ---------------------------------------------------------------------------
class Schema(BaseModel):
    intent: Intent = Field(description="用户意图类型")
    tech_lev: TechLev = Field(description="技术问题的严重程度或级别")


# ---------------------------------------------------------------------------
# 2. 模型：只建一次，避免每个节点重复 new ChatOpenAI
# ---------------------------------------------------------------------------
_llm: Optional[ChatOpenAI] = None


def get_llm() -> ChatOpenAI:
    global _llm
    if _llm is None:
        _llm = ChatOpenAI(
            api_key=os.environ.get("CUSTOM_API_KEY"),
            base_url=os.environ.get("CUSTOM_BASE_URL"),
            model=os.environ.get("CUSTOM_MODEL_NAME"),
        )
    return _llm


# ---------------------------------------------------------------------------
# 3. 节点：只做一件事 —— 写回 state（例如 intent 或追加一条消息）
# ---------------------------------------------------------------------------
_CLASSIFY_PROMPT = (
    f"""你是客服意图分类器，请根据用户输入的意图进行分析，并返回意图分析结果。"""
)


def classify(state: State) -> dict:
    """读 messages，调用 LLM，把 intent 写进 state。"""
    input = [SystemMessage(content=_CLASSIFY_PROMPT), state["messages"][-1]]

    llm = get_llm().with_structured_output(Schema, method="function_calling")
    out = llm.invoke(input)

    print("llm output:", out)
    return {
        "intent": out.intent,
        "tech_lev": out.tech_lev,
    }


def faq_handler(state: State) -> dict:
    return {"messages": [AIMessage(content="[FAQ 分支] 已收到。")]}


def knowledge_base(state: State) -> dict:
    return {"messages": [AIMessage(content="[技术/知识库 分支] 已收到。")]}


def human_handoff(state: State) -> dict:
    return {"messages": [AIMessage(content="[人工/投诉 分支] 已收到。")]}


def knowledge_base_high(state: State) -> dict:
    return {"messages": [AIMessage(content="属于高危技术问题，请转人工处理。")]}


# ---------------------------------------------------------------------------
# 4. 路由函数：只根据当前 state 决定「下一条边」的名字（不写 LLM）
#    必须返回与 add_conditional_edges 第三个参数 dict 的 key 一致
# ---------------------------------------------------------------------------
def route_by_intent(state: State) -> Intent:
    """
    一级路由
    """
    intent = state.get("intent")
    # 防御性编程
    if not intent or intent not in ["faq", "technical", "complaint"]:
        print("警告：LLM 意图识别异常，走默认兜底逻辑")
        intent = "technical"  # 或者返回一个特殊的 default 节点
    return intent


def route_by_technical(state: State) -> TechLev:
    """
    二级路由
    """
    tech_lev = state.get("tech_lev")
    # 防御性编程
    if not tech_lev or tech_lev not in ["high", "low"]:
        print("警告：LLM 意图识别异常，走默认兜底逻辑")
        tech_lev = "high"  # 或者返回一个特殊的 default 节点
    return tech_lev


# ---------------------------------------------------------------------------
# 5. 构图：START → classify → 按 intent 分流 → 各 handler → END
# ---------------------------------------------------------------------------
graph = StateGraph(State)
graph.add_node("classify", classify)
graph.add_node("faq_handler", faq_handler)
graph.add_node("knowledge_base", knowledge_base)
graph.add_node("knowledge_base_high", knowledge_base_high)
graph.add_node("human_handoff", human_handoff)
graph.add_node(
    "tech_router", lambda state: state
)  # 增加一个空节点或者逻辑节点，作为二级路由的载体

graph.add_edge(START, "classify")
graph.add_conditional_edges(
    "classify",
    route_by_intent,
    {
        "faq": "faq_handler",
        "technical": "tech_router",
        "complaint": "human_handoff",
    },
)
graph.add_conditional_edges(
    "tech_router",
    route_by_technical,
    {
        "high": "knowledge_base_high",
        "low": "knowledge_base",
    },
)
graph.add_edge("faq_handler", END)
graph.add_edge("knowledge_base", END)
graph.add_edge("knowledge_base_high", END)
graph.add_edge("human_handoff", END)

app = graph.compile()
# display(Image(app.get_graph().draw_mermaid_png()))
# 不使用图片，直接看文本
# print(app.get_graph().draw_mermaid())
# 只想看图的逻辑，不追求精美图片
# app.get_graph().print_ascii()
# 外部封装
md_code = visualize_graph(app)
print(md_code)

if __name__ == "__main__":
    result = app.invoke({"messages": [HumanMessage(content="1+1=？")], "intent": None})
    print("intent:", result.get("intent"))
    for m in result["messages"]:
        print(m.type, ":", getattr(m, "content", m))

# %%
