# %%
# 🎨 可视化图结构
from IPython.display import Image, display
from langchain_core.messages import HumanMessage
from graph.builder import build_graph
app = build_graph()
display(Image(app.get_graph().draw_mermaid_png()))

import uuid

# 6.Use the graph

cached_human_responses = ["你使用了什么模型？", "q"]
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
        # updates 模式：每项为 {节点名: 该节点写回的状态片段}，无顶层 "messages"
        # 例如 intent_analyzer 只有 intent_data；chitchat/faq 才有 messages
        for _node, patch in output.items():
            msgs = patch.get("messages") if isinstance(patch, dict) else None
            if msgs:
                msgs[-1].pretty_print()

    if output and "prompt" in output:
        print("Done!")



# %%