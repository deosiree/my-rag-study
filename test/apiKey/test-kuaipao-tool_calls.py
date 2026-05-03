from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

# 1. 实例化客户端（只传 key 和 base_url）
client = OpenAI(
    api_key=os.environ.get("GPTMINI_API_KEY"),
    base_url=os.environ.get("GPTMINI_BASE_URL")
)

# 2. 定义一个极简工具
tools = [{
    "type": "function",
    "function": {
        "name": "get_hello",
        "description": "一个打招呼的函数",
        "parameters": {
            "type": "object",
            "properties": {},
            "required": []
        }
    }
}]

try:
    # 3. 在这里传入 model 参数
    response = client.chat.completions.create(
        model=os.environ.get("GPTMINI_MODEL_NAME"),
        messages=[{"role": "user", "content": "请调用 get_hello 函数"}],
        tools=tools,
        tool_choice={"type": "function", "function": {"name": "get_hello"}} # 强制调用测试
    )

    # 4. 检查返回结果
    tool_calls = response.choices[0].message.tool_calls
    if tool_calls:
        print("✅ 恭喜！中转站支持 Function Calling！")
        print(f"返回内容: {tool_calls[0].function}")
    else:
        print("❌ 中转站返回成功，但没有包含 tool_calls，说明不支持工具调用。")

except Exception as e:
    print(f"❌ 请求发生异常: {e}")