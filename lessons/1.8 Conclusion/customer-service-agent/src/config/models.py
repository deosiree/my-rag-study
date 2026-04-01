'''
Author: Spindrift 1692592987@qq.com
Date: 2026-04-01 22:53:01
LastEditors: Spindrift 1692592987@qq.com
LastEditTime: 2026-04-01 22:57:14
FilePath: \my-rag-study\lessons\1.8 Conclusion\customer-service-agent\src\config\models.py
Description: 
'''
import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from schemas.intent import IntentSchema
load_dotenv()


# 基础配置，可以根据环境变量切换模型
def get_model(model_name: str = None, temperature: float = 0.7):
    return ChatOpenAI(
        api_key=os.environ.get("CUSTOM_API_KEY"),
        base_url=os.environ.get("CUSTOM_BASE_URL"),
        model=model_name,
        temperature=temperature,
    )


# 预实例化常用的模型（单例模式思想）
default_llm = get_model(temperature=0.7, model_name=os.environ.get("CUSTOM_MODEL_NAME"))
creative_llm = get_model(temperature=0.9, model_name=os.environ.get("CUSTOM_MODEL_NAME"))  # 需要创作时用
strict_llm = get_model(temperature=0.0, model_name="deepseek-r1:32b") # 需要严格时用
structured_llm = default_llm.with_structured_output(IntentSchema)  # 意图识别专用
