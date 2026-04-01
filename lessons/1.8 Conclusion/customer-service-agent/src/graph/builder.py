"""
Author: Spindrift 1692592987@qq.com
Date: 2026-03-31 23:18:10
LastEditors: Spindrift 1692592987@qq.com
LastEditTime: 2026-04-01 22:59:36
FilePath: \my-rag-study\lessons\1.8 Conclusion\customer-service-agent\src\graph\builder.py
Description: LangGraph 枢纽：建图、连边
    1. 定义节点：每个节点是一个函数，输入是 state，输出是 state；
    2. 定义边：每个边是一个函数，输入是 state，输出是 state；
    3. 定义图：图是节点和边的集合；
    4. 定义图的执行：图的执行是图的节点和边的执行；
    5. 定义图的执行结果：图的执行结果是图的节点和边的执行结果；
    6. 定义图的执行结果的输出：图的执行结果的输出是图的节点和边的执行结果的输出；
"""
from graph.router import router_intent
from graph.state import CustomerServiceState
from langgraph.graph import StateGraph, START, END
from nodes.intentAnalyzerAgent import intent_analyzer_node
from nodes.ragAgent import rag_node
from nodes.chitchatAgent import chitchat_node
from nodes.faqAgent import faq_node
from nodes.humanAgent import human_node
from nodes.clarifyAgent import clarify_node

def build_graph():
    graph = StateGraph(CustomerServiceState)
    graph.add_node("intent_analyzer", intent_analyzer_node)
    graph.add_edge(START, "intent_analyzer")
    graph.add_node("rag", rag_node)
    graph.add_node("chitchat", chitchat_node)
    graph.add_node("faq", faq_node)
    graph.add_node("human", human_node)
    graph.add_node("clarify", clarify_node)
    graph.add_conditional_edges(
        "intent_analyzer",
        router_intent,
        {
            "rag": "rag",# RAG节点
            "chitchat": "chitchat",# 闲聊节点
            "faq": "faq",# FAQ节点
            "human": "human",# 人工节点
            "clarify": "clarify",# 澄清节点
        },
    )
    graph.add_edge("rag", END)
    graph.add_edge("chitchat", END)
    graph.add_edge("faq", END)
    return graph.compile()# 编译图