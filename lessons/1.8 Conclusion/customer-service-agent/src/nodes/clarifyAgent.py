'''
Author: Spindrift 1692592987@qq.com
Date: 2026-04-01 22:46:13
LastEditors: Spindrift 1692592987@qq.com
LastEditTime: 2026-04-01 23:07:10
FilePath: \my-rag-study\lessons\1.8 Conclusion\customer-service-agent\src\nodes\ragAgent.py
Description: 澄清节点，使用澄清技术回答用户问题
'''

from graph.state import CustomerServiceState
from langchain_core.messages import AIMessage


def clarify_node(state: CustomerServiceState):
    """
    description: 澄清节点，使用澄清技术回答用户问题
    return {CustomerServiceState}: 澄清结果
    """
    result = AIMessage(content="这是一个澄清节点")
    return {"messages": [result]}# 返回消息
