# %%
# 🎨 可视化图结构
from IPython.display import Image, display
from langchain_core.messages import HumanMessage
from graph.builder import build_graph
app = build_graph()
display(Image(app.get_graph().draw_mermaid_png()))

import uuid

# 6.Use the graph

cached_human_responses = ["你好吗？能写个自我介绍吗？", "111+111是多少？使用工具进行计算", "我真是服了你了，你能不能不要那么笨啊，重新执行上次任务！", "你使用了什么模型？", "q"]
cached_response_index = 0
config = {"configurable": {"thread_id": str(uuid.uuid4())}}
while True:
    # try:
    #     user = input("User (q/Q to quit): ")
    # except:
    user = cached_human_responses[cached_response_index]
    cached_response_index += 1
    print(f"User (q/Q to quit): {user}")
    if user in {"q", "Q"}:
        print("AI: Byebye")
        break
    output = None
    for output in app.stream(
        {"messages": [HumanMessage(content=user)]}, config=config, stream_mode="updates"
    ):
        print(output)
        # last_message = next(iter(output.values()))["messages"][-1]
        # last_message.pretty_print()

    if output and "prompt" in output:
        print("Done!")



# %%