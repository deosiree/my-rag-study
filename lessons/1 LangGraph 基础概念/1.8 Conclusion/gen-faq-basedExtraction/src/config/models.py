r"""
Author: Spindrift 1692592987@qq.com
Date: 2026-04-01 22:53:01
LastEditors: Spindrift 1692592987@qq.com
LastEditTime: 2026-04-01 22:57:14
FilePath: \my-rag-study\lessons\1.8 Conclusion\customer-service-agent\src\config\models.py
Description:
"""

import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from tools.split_files import split_markdown
from tools.list_files import list_files

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
default_llm = get_model(temperature=0.0, model_name=os.environ.get("CUSTOM_MODEL_NAME"))
default_llm.bind_tools([split_markdown, list_files])
