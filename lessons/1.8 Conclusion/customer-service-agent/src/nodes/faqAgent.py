'''
Author: Spindrift 1692592987@qq.com
Date: 2026-04-01 22:46:13
LastEditors: Spindrift 1692592987@qq.com
LastEditTime: 2026-04-01 23:05:45
FilePath: \my-rag-study\lessons\1.8 Conclusion\customer-service-agent\src\nodes\ragAgent.py
Description: FAQ节点，使用FAQ技术回答用户问题
'''

from config.models import default_llm
from graph.state import CustomerServiceState
from langchain_core.messages import AIMessage


def faq_node(state: CustomerServiceState):
    """
    description: FAQ节点，使用FAQ技术回答用户问题
    return {CustomerServiceState}: FAQ结果
    """
    ai_message = AIMessage(content="这是一个FAQ节点")
    input_messages = state["messages"] + [ai_message]
    result = default_llm.invoke(input_messages)
    return {"messages": [result]}# 返回消息
