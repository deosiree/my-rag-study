'''
Author: Spindrift 1692592987@qq.com
Date: 2026-03-31 23:20:34
LastEditors: Spindrift 1692592987@qq.com
LastEditTime: 2026-04-01 22:43:40
FilePath: \my-rag-study\lessons\1.8 Conclusion\customer-service-agent\src\graph\router.py
Description: 路由决策函数（规则+阈值）
    1. 定义路由决策函数：路由决策函数是一个函数，输入是 state，输出是 state；
'''
from graph.state import CustomerServiceState

def router_intent(state: CustomerServiceState) -> str:
    '''
    description: 路由决策函数，根据意图识别的置信度和歧义情况，决定去向
    return {str}: 路由决策
    '''
    if state.intent_data is None:
        return "human"# 意图识别失败，去人工
    if state.intent_data.confidence < 0.7:
        if state.intent_data.is_ambiguous:
            return "clarify"# 歧义，去澄清
        else:
            return "human"# 置信度低，去人工
    else:
        return state.intent_data.intent_label# 置信度高，去对应的业务节点