from pydantic import BaseModel, Field
from typing import List
from langchain_core.output_parsers import PydanticOutputParser

# 1. 定义单条 FAQ 的结构
class FAQPair(BaseModel):
    # 使用 Field 增加描述，能帮助 LLM 更好地理解字段含义
    question: str = Field(description="用户可能会问的问题，口语化且简短")
    answer: str = Field(description="针对问题的专业、准确解答")

# 2. 定义整个返回列表的结构
class FAQList(BaseModel):
    items: List[FAQPair] = Field(description="提取出来的问答对列表")

# 3. 初始化解析器
parser = PydanticOutputParser(pydantic_object=FAQList)