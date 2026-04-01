'''
Author: Spindrift 1692592987@qq.com
Date: 2026-03-31 23:20:34
LastEditors: Spindrift 1692592987@qq.com
LastEditTime: 2026-04-01 22:45:06
FilePath: \my-rag-study\lessons\1.8 Conclusion\customer-service-agent\src\graph\state.py
Description: 统一 State 定义
    1. 定义 State：State 是一个字典，包含会话状态；
    2. 定义 State 的结构：State 的结构是字典，包含会话状态；
'''
from datetime import datetime
from typing import Optional, TypedDict
from langchain_core.messages import BaseMessage
from langchain_core.runnables import add
from langgraph.graph.message import Annotated, add_messages
from langgraph.graph.state import BaseModel
from schemas.intent import IntentSchema

class CustomerServiceState(TypedDict):
    # 基础：对话历史（包含原始输入）
    messages: Annotated[list, add_messages]
    
    # 核心：意图识别的结构化输出
    # 我们直接定义一个 Pydantic 模型作为“意图结果”
    intent_data: Optional[IntentSchema] 
    
    # 决策：用于条件边（Routing）的简易字段
    next_step: str 