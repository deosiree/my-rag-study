"""
description: 意图分析节点，使用 structured_llm 分析意图
return {CustomerServiceState}: 意图分析结果
"""

from config.models import structured_llm
from graph.state import CustomerServiceState
from schemas.intent import IntentSchema
from langchain_core.messages import SystemMessage


def intent_analyzer_node(state: CustomerServiceState):
    """
    description: 意图分析节点，使用 structured_llm 分析意图
    return {CustomerServiceState}: 意图分析结果
    """
    result = structured_llm.invoke(
        state["messages"],# 用户输入的意图
        SystemMessage(
            content="你是一个意图分析专家，请根据用户输入的意图进行分析，并返回意图分析结果"
        ),# 系统提示词
        prompt=IntentSchema.model_json_schema(),# 意图分析结果的结构化输出
    )
    return {"intent_data": result}# 意图分析结果
