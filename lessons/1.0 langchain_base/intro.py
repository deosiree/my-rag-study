from random import random
from typing import Literal, TypedDict
from langgraph.graph import StateGraph, START, END

# 定义状态
class State(TypedDict):
    graph_state: str

# 定义节点
def node_1(state):
    return {"graph_state": state['graph_state'] + " I am"}

# 定义条件路由
def decide_mood(state) -> Literal["happy", "sad"]:
    return random.choice(["happy", "sad"])

# 构建图
graph = StateGraph(State)
graph.add_node("node_1", node_1)
graph.add_edge(START, "node_1")



graph.add_conditional_edges("node_1", decide_mood)

print("end")