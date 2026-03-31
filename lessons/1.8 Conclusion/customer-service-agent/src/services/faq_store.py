'''
Author: Spindrift 1692592987@qq.com
Date: 2026-03-31 23:20:34
LastEditors: Spindrift 1692592987@qq.com
LastEditTime: 2026-03-31 23:30:40
FilePath: \my-rag-study\lessons\1.8 Conclusion\customer-service-agent\src\services\faq_store.py
Description: FAQ 索引/匹配
    本地 store（FAQ / KB）
        FAQ：用 json/yaml 或小字典就行（问题->答案），先把命中逻辑跑通
        KB：先用本地 md/txt 分段 + 简单检索（甚至先用关键字匹配），后面再换向量库
'''
