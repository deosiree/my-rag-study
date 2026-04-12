"""
description: 意图分析节点，使用 structured_llm 分析意图
return {CustomerServiceState}: 意图分析结果
"""

from config.models import structured_llm
from graph.state import CustomerServiceState
from langchain_core.messages import SystemMessage


def intent_analyzer_node(state: CustomerServiceState):
    """
    description: 意图分析节点，使用 structured_llm 分析意图
    return {CustomerServiceState}: 意图分析结果
    """
    system_message = SystemMessage(
        content="你是一个意图分析专家，请根据用户输入的意图进行分析，并返回意图分析结果"
    )

    input_messages = [system_message] + state["messages"]

    # structured_llm 来自 with_structured_output(IntentSchema)，意图 schema 已经绑在链上了，不需要再手动传一份 JSON Schema
    result = structured_llm.invoke(input_messages)
    return {"intent_data": result}  # 意图分析结果
