'''
Author: Spindrift 1692592987@qq.com
Date: 2026-03-31 23:20:34
LastEditors: Spindrift 1692592987@qq.com
LastEditTime: 2026-03-31 23:31:33
FilePath: \my-rag-study\lessons\1.8 Conclusion\customer-service-agent\src\services\session_memory.py
Description: 会话记忆/上下文管理
    LangGraph 自带记忆能力，用 state 管理会话状态；
    state 用 Pydantic 模型定义，方便序列化/反序列化；
    state 用 LangChain 的 MemorySaver 管理，方便持久化；
    本地 memory（会话）
        先用进程内 dict[session_id] = history/state 就够了
        同时把每轮 state.trace 写到本地文件，方便你复盘“为什么走了这条路”
'''
