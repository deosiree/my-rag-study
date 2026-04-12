"""
初学者的第一个 LangGraph「状态机」
================================
学习顺序（建议配合同目录下 workflow_slides/index.html 幻灯片在浏览器里打开）：

  ① State（TypedDict）——整次运行里「共享的一份字典」
  ② 节点函数——读 state，返回「要合并进 state 的片段」
  ③ 普通边 add_edge——固定先后顺序
  ④ 条件边 add_conditional_edges——像状态机一样分支，再合流

运行：在项目根目录或本目录下执行
  python firstAgent.py
只打印 Mermaid 图（改了节点名后可贴进幻灯片）：
  python firstAgent.py --mermaid
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Literal

from langgraph.graph import END, START, StateGraph
from typing_extensions import NotRequired, TypedDict


# ---------------------------------------------------------------------------
# ① 状态：所有节点读写同一份「形状」；NotRequired 表示一开始可以不填
# ---------------------------------------------------------------------------
class State(TypedDict):
    topic: str
    body: NotRequired[str]
    result: NotRequired[str]


def node_pick_topic(state: State) -> dict:
    """② 节点：只做一件事——规范化 topic（演示「读 state → 返回要更新的键」）。"""
    t = state["topic"].strip()
    return {"topic": t}


def route_by_question(state: State) -> Literal["as_question", "as_fact"]:
    """
    ④ 条件边的路由函数：返回值必须是下面 add_conditional_edges 第三个 dict 里的 key。
    这里用「是否包含问号」模拟简单意图分类（后面可换成 LLM 分类）。
    """
    return "as_question" if "?" in state["topic"] else "as_fact"


def node_question(state: State) -> dict:
    return {
        "body": f"【问题模式】围绕「{state['topic']}」整理引导要点（此处可接 LLM）。"
    }


def node_fact(state: State) -> dict:
    return {
        "body": f"【陈述模式】关于「{state['topic']}」整理说明要点（此处可接 LLM）。"
    }


def node_summary(state: State) -> dict:
    b = state.get("body", "")
    return {
        "result": f"{b}\n→ 流程结束：可把 result 交给前端或下一段 Chain。"
    }


def build_app():
    """组装图：先线性，再分支，再合流——典型的「简单状态机」形状。"""
    g = StateGraph(State)
    g.add_node("pick_topic", node_pick_topic)
    g.add_node("as_question", node_question)
    g.add_node("as_fact", node_fact)
    g.add_node("summary", node_summary)

    g.add_edge(START, "pick_topic")
    g.add_conditional_edges(
        "pick_topic",
        route_by_question,
        {"as_question": "as_question", "as_fact": "as_fact"},
    )
    g.add_edge("as_question", "summary")
    g.add_edge("as_fact", "summary")
    g.add_edge("summary", END)
    return g.compile()


def _strip_mermaid_frontmatter(raw: str) -> str:
    """LangGraph 导出的 Mermaid 可能带 YAML 头，旧版 mermaid.js 可只保留 graph 段。"""
    raw = raw.strip()
    if not raw.startswith("---"):
        return raw
    third = raw.find("---", 3)
    if third == -1:
        return raw
    return raw[third + 3 :].strip()


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description="第一个 LangGraph 状态机示例")
    parser.add_argument(
        "--mermaid",
        action="store_true",
        help="打印 Mermaid 文本（可同步到 workflow_slides/index.html）",
    )
    parser.add_argument(
        "--write-mermaid",
        type=Path,
        metavar="FILE",
        help="把 Mermaid 写入文件（无 YAML 头，便于网页引用）",
    )
    args = parser.parse_args(argv)

    app = build_app()
    mermaid_raw = app.get_graph().draw_mermaid()
    mermaid_clean = _strip_mermaid_frontmatter(mermaid_raw)

    if args.mermaid:
        print(mermaid_clean)
        return

    if args.write_mermaid:
        args.write_mermaid.parent.mkdir(parents=True, exist_ok=True)
        args.write_mermaid.write_text(mermaid_clean + "\n", encoding="utf-8")
        print(f"已写入: {args.write_mermaid.resolve()}")
        return

    # 默认：跑两次，对比「问句 / 非问句」分支
    demos = [
        {"topic": "  什么是 LangGraph？?  "},
        {"topic": "今天学习状态机"},
    ]
    for init in demos:
        out = app.invoke(init)
        print("---")
        print("输入 topic:", repr(init["topic"]))
        print("最终 state:", out)


if __name__ == "__main__":
    try:
        main(sys.argv[1:])
    except KeyboardInterrupt:
        sys.exit(130)
