# %%
# 🎨 可视化图结构
from IPython.display import Image, display
from langchain_core.messages import HumanMessage
from graph.builder import build_graph
app = build_graph()
display(Image(app.get_graph().draw_mermaid_png()))

import uuid

# 6.Use the graph

cached_human_responses = ["你好", "计算111+111", "天空是什么颜色的", "你使用了什么模型？", "q"]
cached_response_index = 0
config = {"configurable": {"thread_id": str(uuid.uuid4())}}
while True:
    # try:
    #     user = input("User (q/Q to quit): ")
    # except:
    user_content = cached_human_responses[cached_response_index]
    cached_response_index += 1
    print(f"User (q/Q to quit): {user_content}")
    if user_content in {"q", "Q"}:
        print("AI: Byebye")
        break
    output = None
    for output in app.stream(
        {"messages": [HumanMessage(content=user_content)]},
        config=config,
        stream_mode="updates",
    ):
        print(output)
        print(type(output))
        print(output.keys())
        print(output.values())
        print(output.items())
        print(output.get("intent_analyzer"))
        print(output.get("chitchat"))
        print(output.get("faq"))
        print(output.get("messages"))
        print(output.get("intent_data"))
        print()

    """
    User (q/Q to quit): 你好
    {'intent_analyzer': {'intent_data': IntentSchema(domain='闲聊', sentiment='中性', intent_label='Chitchat', confidence=0.95, entities={}, is_ambiguous=False, thought='用户输入"你好"是一个简单的问候语，属于典型的闲聊开场白。没有特定的业务需求或问题，只是礼貌性的问候。因此判断为闲聊领域，意图为Chitchat，情绪中性，置信度高，无歧义。')}}
    <class 'dict'>
    dict_keys(['intent_analyzer'])
    dict_values([{'intent_data': IntentSchema(domain='闲聊', sentiment='中性', intent_label='Chitchat', confidence=0.95, entities={}, is_ambiguous=False, thought='用户输入"你好"是一个简单的 问候语，属于典型的闲聊开场白。没有特定的业务需求或问题，只是礼貌性的问候。因此判断为闲聊领域，意图为Chitchat，情绪中性，置信度高，无歧义。')}])
    dict_items([('intent_analyzer', {'intent_data': IntentSchema(domain='闲聊', sentiment='中性', intent_label='Chitchat', confidence=0.95, entities={}, is_ambiguous=False, thought='用户输入"你好"是一个简单的问候语，属于典型的闲聊开场白。没有特定的业务需求或问题，只是礼貌性的问候。因此判断为闲聊领域，意图为Chitchat，情绪中性，置信度高，无歧义。')})])
    {'intent_data': IntentSchema(domain='闲聊', sentiment='中性', intent_label='Chitchat', confidence=0.95, entities={}, is_ambiguous=False, thought='用户输入"你好"是一个简单的问候语，属于典型的闲聊开场白。没有特定的业务需求或问题，只是礼貌性的问候。因此判断为闲聊领域，意图为Chitchat，情绪中性，置信度高，无歧义。')}
    None
    None
    None
    None

    {'chitchat': {'messages': [AIMessage(content='这是一个闲聊节点', additional_kwargs={}, response_metadata={}, id='b36b0227-6c1b-4f1d-845b-f965663a5f6e', tool_calls=[], invalid_tool_calls=[])]}}
    <class 'dict'>
    dict_keys(['chitchat'])
    dict_values([{'messages': [AIMessage(content='这是一个闲聊节点', additional_kwargs={}, response_metadata={}, id='b36b0227-6c1b-4f1d-845b-f965663a5f6e', tool_calls=[], invalid_tool_calls=[])]}])
    dict_items([('chitchat', {'messages': [AIMessage(content='这是一个闲聊节点', additional_kwargs={}, response_metadata={}, id='b36b0227-6c1b-4f1d-845b-f965663a5f6e', tool_calls=[], invalid_tool_calls=[])]})])
    None
    {'messages': [AIMessage(content='这是一个闲聊节点', additional_kwargs={}, response_metadata={}, id='b36b0227-6c1b-4f1d-845b-f965663a5f6e', tool_calls=[], invalid_tool_calls=[])]}        
    None
    None
    None

    User (q/Q to quit): 计算111+111
    {'intent_analyzer': {'intent_data': IntentSchema(domain='计算', sentiment='中性', intent_label='FAQ', confidence=0.9, entities={}, is_ambiguous=False, thought='用户输入"计算111+111"是一 个明确的数学计算请求。这是一个常见问题解答类型的请求，用户希望得到一个具体的计算结果。没有情感色彩，属于中性情绪。这是一个明确的意图，没有歧义。')}}
    <class 'dict'>
    dict_keys(['intent_analyzer'])
    dict_values([{'intent_data': IntentSchema(domain='计算', sentiment='中性', intent_label='FAQ', confidence=0.9, entities={}, is_ambiguous=False, thought='用户输入"计算111+111"是一个明确的数学计算请求。这是一个常见问题解答类型的请求，用户希望得到一个具体的计算结果。没有情感色彩，属于中性情绪。这是一个明确的意图，没有歧义。')}])
    dict_items([('intent_analyzer', {'intent_data': IntentSchema(domain='计算', sentiment='中性', intent_label='FAQ', confidence=0.9, entities={}, is_ambiguous=False, thought='用户输入"计算111+111"是一个明确的数学计算请求。这是一个常见问题解答类型的请 求，用户希望得到一个具体的计算结果。没有情感色彩，属于中性情绪。这是一个明确的意图，没有歧义。')})])
    {'intent_data': IntentSchema(domain='计算', sentiment='中性', intent_label='FAQ', confidence=0.9, entities={}, is_ambiguous=False, thought='用户输入"计算111+111"是一个明确的数学计算请求 。这是一个常见问题解答类型的请求，用户希望得到一个具体的计算结果。没有情感色彩，属于中性情绪。这是一个明确的意图，没有歧义。')}
    None
    None
    None
    None

    {'faq': {'messages': [AIMessage(content='这是一个FAQ节点', additional_kwargs={}, response_metadata={}, id='26f21c6f-e0b6-495c-a8e5-6cfc6d22d689', tool_calls=[], invalid_tool_calls=[])]}}
    <class 'dict'>
    dict_keys(['faq'])
    dict_values([{'messages': [AIMessage(content='这是一个FAQ节点', additional_kwargs={}, response_metadata={}, id='26f21c6f-e0b6-495c-a8e5-6cfc6d22d689', tool_calls=[], invalid_tool_calls=[])]}])
    dict_items([('faq', {'messages': [AIMessage(content='这是一个FAQ节点', additional_kwargs={}, response_metadata={}, id='26f21c6f-e0b6-495c-a8e5-6cfc6d22d689', tool_calls=[], invalid_tool_calls=[])]})])
    None
    None
    {'messages': [AIMessage(content='这是一个FAQ节点', additional_kwargs={}, response_metadata={}, id='26f21c6f-e0b6-495c-a8e5-6cfc6d22d689', tool_calls=[], invalid_tool_calls=[])]}
    None
    None

    User (q/Q to quit): 天空是什么颜色的
    {'intent_analyzer': {'intent_data': IntentSchema(domain='闲聊', sentiment='中性', intent_label='Chitchat', confidence=0.95, entities={}, is_ambiguous=False, thought='用户询问"天空是什么 颜色的"，这是一个关于自然现象的基本问题，属于闲聊范畴。用户情 绪中性，没有明显的业务需求或技术支持意图。这是一个明确的闲聊意图，询问常识性问题，没有歧义。')}}
    <class 'dict'>
    dict_keys(['intent_analyzer'])
    dict_values([{'intent_data': IntentSchema(domain='闲聊', sentiment='中性', intent_label='Chitchat', confidence=0.95, entities={}, is_ambiguous=False, thought='用户询问"天空是什么颜色的" ，这是一个关于自然现象的基本问题，属于闲聊范畴。用户情绪中性，没有明显的业务需求或技术支持意图。这是一个明确的闲聊意图，询问常识性问题，没有歧义。')}])
    dict_items([('intent_analyzer', {'intent_data': IntentSchema(domain='闲聊', sentiment='中性', intent_label='Chitchat', confidence=0.95, entities={}, is_ambiguous=False, thought='用户询问"天空是什么颜色的"，这是一个关于自然现象的基本问题，属于闲聊范畴。用户情绪中性，没有明显的业务需求或技术支持意图。这是一个明确的闲聊意图，询问常识性问题，没有歧义。')})])
    {'intent_data': IntentSchema(domain='闲聊', sentiment='中性', intent_label='Chitchat', confidence=0.95, entities={}, is_ambiguous=False, thought='用户询问"天空是什么颜色的"，这是一个关于自然现象的基本问题，属于闲聊范畴。用户情绪中性，没有明显的业务需求或技术支持意图。这是一个明确的闲聊意图，询问常识性问题，没有歧义。')}
    None
    None
    None
    None

    {'chitchat': {'messages': [AIMessage(content='这是一个闲聊节点', additional_kwargs={}, response_metadata={}, id='aa55ac2b-0f4e-4e41-a62b-29921978dd9d', tool_calls=[], invalid_tool_calls=[])]}}
    <class 'dict'>
    dict_keys(['chitchat'])
    dict_values([{'messages': [AIMessage(content='这是一个闲聊节点', additional_kwargs={}, response_metadata={}, id='aa55ac2b-0f4e-4e41-a62b-29921978dd9d', tool_calls=[], invalid_tool_calls=[])]}])
    dict_items([('chitchat', {'messages': [AIMessage(content='这是一个闲聊节点', additional_kwargs={}, response_metadata={}, id='aa55ac2b-0f4e-4e41-a62b-29921978dd9d', tool_calls=[], invalid_tool_calls=[])]})])
    None
    {'messages': [AIMessage(content='这是一个闲聊节点', additional_kwargs={}, response_metadata={}, id='aa55ac2b-0f4e-4e41-a62b-29921978dd9d', tool_calls=[], invalid_tool_calls=[])]}        
    None
    None
    None

    User (q/Q to quit): 你使用了什么模型？
    {'intent_analyzer': {'intent_data': IntentSchema(domain='技术 支持', sentiment='中性', intent_label='FAQ', confidence=0.85, entities={}, is_ambiguous=False, thought='用户询问"你使用了什 么模型？"，这是一个关于AI助手技术实现的问题。用户想知道当前对 话系统使用的底层模型或技术架构。这属于常见问题解答(FAQ)范畴， 用户情绪中性，没有表达不满或急切。问题明确，没有歧义，用户是在询问技术细节而非寻求其他服务。')}}
    <class 'dict'>
    dict_keys(['intent_analyzer'])
    dict_values([{'intent_data': IntentSchema(domain='技术支持', sentiment='中性', intent_label='FAQ', confidence=0.85, entities={}, is_ambiguous=False, thought='用户询问"你使用了什么模型？"，这是一个关于AI助手技术实现的问题。用户想知道当前对话系统使用的底层模型或技术架构。这属于常见问题解答(FAQ)范畴，用户情绪中 性，没有表达不满或急切。问题明确，没有歧义，用户是在询问技术细节而非寻求其他服务。')}])
    dict_items([('intent_analyzer', {'intent_data': IntentSchema(domain='技术支持', sentiment='中性', intent_label='FAQ', confidence=0.85, entities={}, is_ambiguous=False, thought='用户询问"你使用了什么模型？"，这是一个关于AI助手技术实现的问题。用户想 知道当前对话系统使用的底层模型或技术架构。这属于常见问题解答(FAQ)范畴，用户情绪中性，没有表达不满或急切。问题明确，没有歧义 ，用户是在询问技术细节而非寻求其他服务。')})])
    {'intent_data': IntentSchema(domain='技术支持', sentiment='中 性', intent_label='FAQ', confidence=0.85, entities={}, is_ambiguous=False, thought='用户询问"你使用了什么模型？"，这是一个关于AI助手技术实现的问题。用户想知道当前对话系统使用的底层模型或技术架构。这属于常见问题解答(FAQ)范畴，用户情绪中性，没有表达 不满或急切。问题明确，没有歧义，用户是在询问技术细节而非寻求其他服务。')}
    None
    None
    None
    None

    {'faq': {'messages': [AIMessage(content='这是一个FAQ节点', additional_kwargs={}, response_metadata={}, id='ba4a21a4-a6aa-4a2b-bdb5-8d1022c8456c', tool_calls=[], invalid_tool_calls=[])]}}
    <class 'dict'>
    dict_keys(['faq'])
    dict_values([{'messages': [AIMessage(content='这是一个FAQ节点', additional_kwargs={}, response_metadata={}, id='ba4a21a4-a6aa-4a2b-bdb5-8d1022c8456c', tool_calls=[], invalid_tool_calls=[])]}])
    dict_items([('faq', {'messages': [AIMessage(content='这是一个FAQ节点', additional_kwargs={}, response_metadata={}, id='ba4a21a4-a6aa-4a2b-bdb5-8d1022c8456c', tool_calls=[], invalid_tool_calls=[])]})])
    None
    None
    {'messages': [AIMessage(content='这是一个FAQ节点', additional_kwargs={}, response_metadata={}, id='ba4a21a4-a6aa-4a2b-bdb5-8d1022c8456c', tool_calls=[], invalid_tool_calls=[])]}
    None
    None

    User (q/Q to quit): q
    AI: Byebye
    """

# %%