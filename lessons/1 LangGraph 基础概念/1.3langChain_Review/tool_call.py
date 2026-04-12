import os
from typing import Any

import httpx
from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain.tools import tool
from langchain_core.messages import AIMessage, AIMessageChunk, ToolMessage
from langchain_openai import ChatOpenAI

load_dotenv()  # 这一行会把 .env 的值加载到 os.environ

# 1. 初始化你已经在 .env 中配置好的 DeepSeek 模型
llm = ChatOpenAI(
    api_key=os.environ.get("CUSTOM_API_KEY"),
    base_url=os.environ.get("CUSTOM_BASE_URL"),
    model=os.environ.get("CUSTOM_MODEL_NAME"),  # 确保这里是 deepseek-chat 或相关名称
)

# --- 天气工具：用公开 HTTP API 拉取事实数据（推荐做法）---
# 若目标是「搜索引擎式」泛检索（新闻/多站点摘要），可改用 Tavily / SerpAPI 等，再把摘要交给模型；
# 若目标是「某地当前天气」这类结构化事实，优先调用天气/地理编码 API（如 Open-Meteo），比解析 SERP 网页更稳、更省 token。
_GEOCODE = "https://geocoding-api.open-meteo.com/v1/search"
_FORECAST = "https://api.open-meteo.com/v1/forecast"
_WMO_ZH: dict[int, str] = {
    0: "晴",
    1: "大部晴朗",
    2: "局部多云",
    3: "阴",
    45: "雾",
    48: "雾凇雾",
    51: "小毛毛雨",
    53: "中毛毛雨",
    55: "大毛毛雨",
    61: "小雨",
    63: "中雨",
    65: "大雨",
    71: "小雪",
    73: "中雪",
    75: "大雪",
    80: "阵雨",
    81: "强阵雨",
    82: "暴雨性阵雨",
    95: "雷暴",
    96: "雷暴伴冰雹",
    99: "强雷暴伴冰雹",
}


def _wmo_zh(code: int | None) -> str:
    if code is None:
        return "未知"
    return _WMO_ZH.get(int(code), f"天气码 {code}")


@tool
def get_weather(location: str) -> str:
    """根据地名或城市名查询当前天气（气温、天气状况、湿度、风速）。

    Args:
        location: 地点，可用中文或英文，如「北京」「San Francisco」。
    """
    params_geo: dict[str, Any] = {
        "name": location.strip(),
        "count": 1,
        "language": "zh",
    }
    try:
        with httpx.Client(timeout=15.0) as client:
            # 获取地点信息
            r = client.get(_GEOCODE, params=params_geo)
            r.raise_for_status()  # 检查请求是否成功
            geo = r.json()
            results = geo.get("results") or []  # 获取地点列表
            if not results:
                return f"未找到地点「{location}」，请换更具体的名称（含国家/省）再试。"
            # 根据地点信息获取天气数据
            top = results[0]  # 获取第一个地点
            lat, lon = top["latitude"], top["longitude"]  # 获取经纬度
            name = top.get("name", location)  # 获取地点名称
            country = top.get("country_code", "")  # 获取国家代码

            params_fc: dict[str, Any] = {  # 设置天气参数
                "latitude": lat,  # 设置纬度
                "longitude": lon,  # 设置经度
                "current": "temperature_2m,relative_humidity_2m,weather_code,wind_speed_10m",  # 设置当前天气参数
                "timezone": "auto",  # 设置时区
            }
            r2 = client.get(_FORECAST, params=params_fc)  # 获取天气数据
            r2.raise_for_status()  # 检查请求是否成功
            cur = r2.json().get("current") or {}  # 获取当前天气数据
    except httpx.HTTPError as e:
        return f"天气服务请求失败：{e!s}"

    temp = cur.get("temperature_2m")
    hum = cur.get("relative_humidity_2m")
    code = cur.get("weather_code")
    wind = cur.get("wind_speed_10m")
    desc = _wmo_zh(code)
    place = f"{name}" + (f" ({country})" if country else "")
    parts = [
        f"{place} 当前：{desc}",
        f"气温约 {temp}°C" if temp is not None else None,
        f"相对湿度 {hum}%" if hum is not None else None,
        f"10m 风速约 {wind} km/h" if wind is not None else None,
    ]
    return "，".join(p for p in parts if p)


def print_agent_updates_pretty(chunk: dict[str, Any]) -> None:
    """解析 create_agent + stream_mode='updates' 的 dict，便于阅读（不是 StrOutputParser 的职责）。"""
    for node, payload in chunk.items():
        msgs = payload.get("messages", []) if isinstance(payload, dict) else []
        if node == "model":
            for m in msgs:
                if not isinstance(m, AIMessage):
                    continue
                if m.content:
                    print(f"  · 模型: {m.content}")
                for tc in m.tool_calls or []:
                    name = tc.get("name", "?")
                    args = tc.get("args", {})
                    print(f"  · 调用工具: {name}({args})")
        elif node == "tools":
            for m in msgs:
                if isinstance(m, ToolMessage):
                    print(f"  · 工具结果 [{m.name}]: {m.content}")
        else:
            print(f"  · [{node}] {payload}")


def _unwrap_messages_stream_event(event: Any) -> tuple[Any, dict[str, Any]]:
    """stream_mode='messages' 时，事件多为 (message, metadata)，少数环境下可能直接是 message。"""
    if isinstance(event, tuple) and len(event) == 2 and isinstance(event[1], dict):
        return event[0], event[1]
    return event, {}


# 2. 将 llm 对象传入 agent
# 注意：这里不再传字符串，而是传 llm 实例
agent = create_agent(
    model=llm,
    tools=[get_weather],
)

# 3. 走 Agent 才会用工具：llm.stream() 只是「裸调模型」，不会加载 tools，也没有「调用工具再回答」的循环。
#    create_agent 已在内部搭好状态机（等价于你手写 LangGraph 的 model / tool 节点与边），无需再 add_node/add_edge，
#    但必须用 agent.invoke / agent.stream 入口，不能把 agent 晾在一边又去调 llm。
_user_weather = {
    "messages": [
        {"role": "user", "content": "请查询南京当前天气，用工具查到的结果简要回答。"}
    ]
}

print("—— 裸 LLM（不会调 get_weather）：", end="")
for chunk in llm.stream("请查询南京当前天气，用工具查到的结果简要回答。"):
    print(chunk.content, end="", flush=True)
print()

print("—— Agent（会按需调工具）：")
for chunk in agent.stream(_user_weather, stream_mode="updates"):
    print(chunk, end="", flush=True)
    print()

print("—— Agent（会按需调工具），逐步骤格式化输出：")
for chunk in agent.stream(_user_weather, stream_mode="updates"):
    print_agent_updates_pretty(chunk)
    print("  ---")

# StrOutputParser 用于「线性链」如 prompt | llm | StrOutputParser()，把单条模型输出转成 str；
# Agent 图流式输出是多节点 state 更新，需像上面这样解析 dict，或下面这样只要最终一句。
# 下列 invoke 与上方 stream 会各跑一遍 Agent，生产环境请二选一以免重复计费。
print("—— 仅最终回复（invoke + 最后一条 AIMessage）：")
_final = agent.invoke(_user_weather)
_last = _final["messages"][-1]
if isinstance(_last, AIMessage) and _last.content:
    print(_last.content)
else:
    print(_last)

# 流式必须用 stream / astream，不能用 invoke：invoke 只返回最终 state，不会按 token 推送。
# stream_mode="messages"：LLM 在图里每次生成会产出 (AIMessageChunk, metadata)，metadata["langgraph_node"]
# 为 "model" 或 "tools"；打字机效果只打印 model 节点里带 content 的文本块。
print("—— Agent stream_mode=\"messages\"（模型分块打字机 + 工具结果分行）：")
for event in agent.stream(_user_weather, stream_mode="messages"):
    msg, meta = _unwrap_messages_stream_event(event)
    node = meta.get("langgraph_node", "")
    if node == "model" and isinstance(msg, AIMessageChunk) and msg.content:
        print(msg.content, end="", flush=True)
    elif node == "tools" and isinstance(msg, ToolMessage):
        print(f"\n[工具 {msg.name}] {msg.content}\n", end="", flush=True)
print()
