'''
Author: Spindrift 1692592987@qq.com
Date: 2026-04-12 20:46:37
LastEditors: Spindrift 1692592987@qq.com
LastEditTime: 2026-04-12 21:16:21
FilePath: \my-rag-study\lessons\2 Agent-Chain-Router\2.0 Introduction\clientServer.py
Description: LangGraph 示例 — 用 LLM 做意图分类，再按 intent 路由到不同节点（无大模型时可将 classify 换成规则函数）。
'''
# %%
# 🎨 可视化图结构
from IPython.display import Image, display
import os
from typing import Literal, Optional, TypedDict

from dotenv import load_dotenv
from langchain_core.messages import AIMessage, BaseMessage, HumanMessage
from langchain_openai import ChatOpenAI
from langgraph.graph import END, START, StateGraph

load_dotenv()

# ---------------------------------------------------------------------------
# 1. 状态：图里流转的唯一数据结构（节点返回值会 merge 进这里）
# ---------------------------------------------------------------------------
Intent = Literal["faq", "technical", "complaint"]


class State(TypedDict):
    messages: list[BaseMessage]
    intent: Optional[Intent]


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
_CLASSIFY_PROMPT = """你是客服意图分类器。根据用户最后一句话，只输出下面三个词之一，不要其它内容：
faq | technical | complaint
含义：faq=常见问题；technical=技术/产品问题；complaint=投诉或强烈不满。"""


def classify(state: State) -> dict:
    """读 messages，调用 LLM，把 intent 写进 state。"""
    last = state["messages"][-1]
    user_text = last.content if isinstance(last.content, str) else str(last.content)
    llm = get_llm()
    out = llm.invoke(
        [
            HumanMessage(content=_CLASSIFY_PROMPT),
            HumanMessage(content=user_text),
        ]
    )
    print("llm output:", out)
    raw = (out.content or "").strip().lower()
    if "faq" in raw:
        intent: Intent = "faq"
    elif "complaint" in raw:
        intent = "complaint"
    elif "technical" in raw:
        intent = "technical"
    else:
        intent = "faq"
    return {"intent": intent}


def faq_handler(state: State) -> dict:
    return {"messages": state["messages"] + [AIMessage(content="[FAQ 分支] 已收到。")]}


def knowledge_base(state: State) -> dict:
    return {"messages": state["messages"] + [AIMessage(content="[技术/知识库 分支] 已收到。")]}


def human_handoff(state: State) -> dict:
    return {"messages": state["messages"] + [AIMessage(content="[人工/投诉 分支] 已收到。")]}


# ---------------------------------------------------------------------------
# 4. 路由函数：只根据当前 state 决定「下一条边」的名字（不写 LLM）
#    必须返回与 add_conditional_edges 第三个参数 dict 的 key 一致
# ---------------------------------------------------------------------------
def route_by_intent(state: State) -> Intent:
    assert state.get("intent") is not None
    return state["intent"]


# ---------------------------------------------------------------------------
# 5. 构图：START → classify → 按 intent 分流 → 各 handler → END
# ---------------------------------------------------------------------------
graph = StateGraph(State)
graph.add_node("classify", classify)
graph.add_node("faq_handler", faq_handler)
graph.add_node("knowledge_base", knowledge_base)
graph.add_node("human_handoff", human_handoff)

graph.add_edge(START, "classify")
graph.add_conditional_edges(
    "classify",
    route_by_intent,
    {
        "faq": "faq_handler",
        "technical": "knowledge_base",
        "complaint": "human_handoff",
    },
)
graph.add_edge("faq_handler", END)
graph.add_edge("knowledge_base", END)
graph.add_edge("human_handoff", END)

app = graph.compile()
display(Image(app.get_graph().draw_mermaid_png()))


if __name__ == "__main__":
    result = app.invoke(
        {"messages": [HumanMessage(content="你们退款政策是什么？")], "intent": None}
    )
    print("intent:", result.get("intent"))
    for m in result["messages"]:
        print(m.type, ":", getattr(m, "content", m))

# %%
