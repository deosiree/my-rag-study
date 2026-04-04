from typing import Literal, TypedDict
from pydantic import BaseModel, Field

class EntitySlots(TypedDict, total=False):
    order_id: str
    product_id: str
    user_id: str
class IntentSchema(BaseModel):
    """意图识别的完整结论"""
    # 维度分析（作为中间推理，引导模型想清楚）
    domain: str = Field(description="业务领域，如：订单、技术支持、闲聊")
    sentiment: str = Field(description="用户情绪：积极、中性、愤怒")
    
    # 最终输出
    intent_label: Literal['FAQ', 'KB', 'Human', 'Chitchat', 'Clarify'] = Field(description="标准意图标签")
    confidence: float = Field(description="置信度 0-1")
    entities: EntitySlots = Field(default_factory=dict, description="提取到的实体槽位")# `['order_id', 'product_id', 'user_id']`
    is_ambiguous: bool = Field(description="是否歧义")
    thought: str = Field(description="推理链路")