import os
from langgraph.graph import StateGraph, START, END
from langchain_openai import ChatOpenAI
from typing import TypedDict
from dotenv import load_dotenv

load_dotenv() # 这一行会把 .env 的值加载到 os.environ

class State(TypedDict):
    question: str
    answer: str


def answer_node(state: State):
    llm = ChatOpenAI(
        api_key=os.environ.get("CUSTOM_API_KEY"),
        base_url=os.environ.get("CUSTOM_BASE_URL"),
        model=os.environ.get("CUSTOM_MODEL_NAME")
    )
    response = llm.invoke(state["question"])
    return {"answer": response.content}


api_key = os.environ.get("CUSTOM_API_KEY")
base_url = os.environ.get("CUSTOM_BASE_URL")
model = os.environ.get("CUSTOM_MODEL_NAME")
print(api_key, base_url, model)

graph = StateGraph(State)
graph.add_node("answer_node", answer_node)
graph.add_edge(START, "answer_node")
graph.add_edge("answer_node", END)

app = graph.compile()
result = app.invoke({"question": "什么是 LangGraph？"})
print(result["answer"])
