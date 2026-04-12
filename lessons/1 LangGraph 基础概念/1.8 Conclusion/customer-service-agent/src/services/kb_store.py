'''
Author: Spindrift 1692592987@qq.com
Date: 2026-03-31 23:20:34
LastEditors: Spindrift 1692592987@qq.com
LastEditTime: 2026-03-31 23:30:25
FilePath: \my-rag-study\lessons\1.8 Conclusion\customer-service-agent\src\services\kb_store.py
Description: 向量库/文档库访问
    知识库/文档库访问：LLM 只能处理文本，需要先加载到内存；
    向量库/文档库访问：使用 Embedding 将文本转换为向量，再使用向量搜索；
    文档库访问：使用本地文件系统或云存储访问文档；
    向量库访问：使用向量数据库访问向量；
    本地 store（FAQ / KB）
        FAQ：用 json/yaml 或小字典就行（问题->答案），先把命中逻辑跑通
        KB：先用本地 md/txt 分段 + 简单检索（甚至先用关键字匹配），后面再换向量库
'''
