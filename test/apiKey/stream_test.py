import os
from openai import OpenAI

# 自动使用你配置的服务商和模型
client = OpenAI(
    api_key=os.environ.get("CUSTOM_API_KEY") or os.environ.get("OPENAI_API_KEY"),
    base_url=os.environ.get("CUSTOM_BASE_URL", "https://api.openai.com/v1")
)

model = os.environ.get("CUSTOM_MODEL_NAME", "gpt-4o-mini")

# stream=True 启用流式输出，配合后端 SSE 实时推送每个 token
stream = client.chat.completions.create(
    model=model,
    messages=[{"role": "user", "content": "你好，请用一句话介绍你自己！"}],
    stream=True
)

print(f"[{model}] ", end="", flush=True)
for chunk in stream:
    if chunk.choices[0].delta.content:
        print(chunk.choices[0].delta.content, end="", flush=True)
print()