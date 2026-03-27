# 我的 LangGraph 模板
from langgraph.graph import StateGraph, START, END
from typing_extensions import TypedDict,NotRequired
from typing import Literal
from datetime import datetime

class State(TypedDict):
    # 定义你的状态
    topic: str
    body: NotRequired[str]
    result: NotRequired[str]

def node_topic(state: State) -> dict:
    # 实现你的逻辑
    return {"topic": state["topic"].strip()}

def node_day(state: State) -> dict:
    # 实现你的逻辑
    date = datetime.now()
    return {"body": f"时间单位：日，今天是{date}"}

def node_month(state: State) -> dict:
    # 实现你的逻辑
    date = datetime.now().month
    return {"body": f"时间单位：月，现在是{date}月"}

def node_year(state: State) -> dict:
    # 实现你的逻辑
    date = datetime.now().year
    return {"body": f"时间单位：年，现在是{date}年"}

def node_result(state: State) -> dict:
    # 实现你的逻辑
    body = state["body"] if state["body"] else "没有匹配到时间单位"
    return {"result": f"经条件判断：{body}"}

def route_node_by_time(state:State) -> Literal["node_day", "node_month", "node_year"]:
    if state["topic"].find("日") != -1:
        return "node_day"
    elif state["topic"].find("月") != -1:
        return "node_month"
    elif state["topic"].find("年") != -1:
        return "node_year"
    else:
        return "node_result"
def build_app():
    graph = StateGraph(State)
    graph.add_node("node_topic", node_topic)
    graph.add_node("node_day", node_day)
    graph.add_node("node_month", node_month)
    graph.add_node("node_year", node_year)
    graph.add_node("node_result", node_result)
    graph.add_conditional_edges("node_topic", route_node_by_time,{"node_day": "node_day", "node_month": "node_month", "node_year": "node_year", "node_result": "node_result"})
    graph.add_edge(START, "node_topic")
    graph.add_edge("node_day", "node_result")
    graph.add_edge("node_month", "node_result")
    graph.add_edge("node_year", "node_result")
    graph.add_edge("node_result", END)
    return graph.compile()

def main():
    app = build_app()
    question = input("请询问日期：")
    initial_state = {"topic": question}
    result = app.invoke(initial_state)
    print(result)

if __name__ == "__main__":
    main()
