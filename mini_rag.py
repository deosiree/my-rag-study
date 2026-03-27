from get_emb import CosineSimilarityRetriever, QianwenChat

kb = [
    "OpenViking 默认端口是 1933",
    "Gemini 建议使用 Flash 模型省钱",
    "Brave 搜索需要海外信用卡支付",
]

query = "OpenViking 端口是多少？"

retriever = CosineSimilarityRetriever()
best_doc, scores = retriever.retrieve(query, kb)

prompt = f"已知信息：{best_doc}\n问题：{query}\n请根据已知信息回答。"
print("prompt:", prompt)

llm = QianwenChat()
answer = llm.complete(prompt)

print(f"--- 检索到的资料 ---\n{best_doc}")
print(f"--- 各条余弦相似度（便于对照学习）---\n{list(zip(kb, scores))}")
print(f"--- AI 的回答 ---\n{answer}")
