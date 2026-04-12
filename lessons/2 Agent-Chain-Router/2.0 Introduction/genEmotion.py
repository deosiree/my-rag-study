"""
Author: Spindrift 1692592987@qq.com
Date: 2026-04-12 20:09:40
LastEditors: Spindrift 1692592987@qq.com
LastEditTime: 2026-04-12 20:25:16
FilePath: \my-rag-study\lessons\2 Agent-Chain-Router\2.0 Introduction\genEmotion.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
"""

from langgraph.graph import START, END, StateGraph
from typing import TypedDict
import random

class State(TypedDict):
    text: str
    emotion: str

def add_happy(state: State):
    return {"emotion": "happy"}


def add_sad(state: State):
    return {"emotion": "sad"}


def add_neutral(state: State):
    return {"emotion": "neutral"}


def router(state: State):
    emotion = random.choice(["happy", "sad", "neutral"])
    if emotion == "happy":
        return "add_happy"
    elif emotion == "sad":
        return "add_sad"
    elif emotion == "neutral":
        return "add_neutral"
    else:
        return "add_neutral"


def combine_text(state: State):
    return {"text": state["text"] + state["emotion"]}


graph = StateGraph(State)
graph.add_node("add_happy", add_happy)
graph.add_node("add_sad", add_sad)
graph.add_node("add_neutral", add_neutral)
graph.add_node("combine_text", combine_text)
graph.add_conditional_edges(
    START,
    router,
    {"add_happy": "add_happy", "add_sad": "add_sad", "add_neutral": "add_neutral"},
)
graph.add_edge("add_happy", "combine_text")
graph.add_edge("add_sad", "combine_text")
graph.add_edge("add_neutral", "combine_text")
graph.add_edge("combine_text", END)
app = graph.compile()

print(app.invoke({"text": "I am "})["text"])
