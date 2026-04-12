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


# =============================================================================
# ① stream_mode="updates"：仅本段函数互相调用，与其它模式无关
#    每条 event：dict，如 {"model": {"messages": [AIMessage, ...]}, ...}
# =============================================================================


def updates_print_ai_message_line(node_name: str, m: AIMessage) -> None:
    if m.content:
        print(f"  [{node_name}] 模型: {m.content}")
    for tc in m.tool_calls or []:
        print(f"  [{node_name}] 调工具: {tc.get('name')} {tc.get('args')}")


def updates_print_tool_message_line(node_name: str, m: ToolMessage) -> None:
    print(f"  [{node_name}] 工具[{m.name}]: {m.content}")


def updates_print_other_message_line(node_name: str, m: Any) -> None:
    print(f"  [{node_name}] {type(m).__name__}: {getattr(m, 'content', m)!r}")


def updates_print_messages_under_node(node_name: str, diff: dict[str, Any]) -> None:
    for m in diff.get("messages", []):
        if isinstance(m, AIMessage):
            updates_print_ai_message_line(node_name, m)
        elif isinstance(m, ToolMessage):
            updates_print_tool_message_line(node_name, m)
        else:
            updates_print_other_message_line(node_name, m)


def print_updates_str_mode(chunk: dict[str, Any]) -> None:
    """入口：``for ev in agent.stream(..., stream_mode="updates"): print_updates_str_mode(ev)``"""
    for node_name, diff in chunk.items():
        if not isinstance(diff, dict) or "messages" not in diff:
            print(f"  [{node_name}] {diff!r}")
            continue
        updates_print_messages_under_node(node_name, diff)


# =============================================================================
# ② stream_mode="messages"：仅本段函数互相调用
#    每条 event：(消息, meta)。分流用 isinstance 即可：模型流是 AIMessageChunk，工具是 ToolMessage。
#    meta["langgraph_node"] 与类型基本同义，仅排障或复杂图时再看 meta。
# =============================================================================


def messages_print_model_chunk(msg: AIMessageChunk) -> None:
    if msg.content:
        print(msg.content, end="", flush=True)
    elif getattr(msg, "tool_calls", None):
        print(f"\n  [model] tool_calls={msg.tool_calls!r}")


def messages_print_tool_chunk(msg: ToolMessage) -> None:
    print(f"\n  [tools] {msg.name}: {msg.content}")


def messages_print_fallback(msg: Any, meta: Any) -> None:
    print(f"\n  [其它类型] {type(msg).__name__} {msg!r}  meta={meta!r}")


def print_messages_str_mode(ev: tuple[Any, Any]) -> None:
    """入口：``for ev in agent.stream(..., stream_mode="messages"): print_messages_str_mode(ev)``"""
    msg, meta = ev[0], ev[1]
    if isinstance(msg, AIMessageChunk):
        messages_print_model_chunk(msg)
    elif isinstance(msg, ToolMessage):
        messages_print_tool_chunk(msg)
    else:
        messages_print_fallback(msg, meta)


# =============================================================================
# ③ stream_mode="values"：仅本段函数互相调用
#    每条 event：全量 state dict
# =============================================================================


def values_format_message_preview(m: Any) -> str:
    preview = getattr(m, "content", "") or ""
    if len(preview) > 120:
        preview = preview[:117] + "..."
    return f"{type(m).__name__} | {preview!r}"


def values_print_state_header(state: dict[str, Any]) -> None:
    msgs = state.get("messages", [])
    print(f"  state 键: {list(state.keys())} | messages 条数: {len(msgs)}")


def print_values_str_mode(state: dict[str, Any]) -> None:
    """入口：``for ev in agent.stream(..., stream_mode="values"): print_values_str_mode(ev)``"""
    values_print_state_header(state)
    msgs = state.get("messages", [])
    if msgs:
        print(f"  最后一条: {values_format_message_preview(msgs[-1])}")


# =============================================================================
# ④ stream_mode="custom"：仅本段（StreamWriter 写入的数据）
# =============================================================================


def custom_payload_repr(payload: Any) -> str:
    return repr(payload)


def print_custom_str_mode(payload: Any) -> None:
    """入口：``for ev in agent.stream(..., stream_mode="custom"): print_custom_str_mode(ev)``"""
    print(f"  custom: {custom_payload_repr(payload)}")


# =============================================================================
# ⑤ stream_mode="debug"
# =============================================================================


def debug_short_repr(payload: Any, max_len: int = 500) -> str:
    s = repr(payload)
    return s if len(s) <= max_len else s[: max_len - 3] + "..."


def print_debug_str_mode(payload: Any) -> None:
    """入口：``for ev in agent.stream(..., stream_mode="debug"): print_debug_str_mode(ev)``"""
    print(f"  debug: {debug_short_repr(payload)}")


# --- 若使用 stream_mode=["updates"] 等列表形态，可先取 event[1] 再传入上面各 print_*_str_mode ---
def unwrap_stream_payload(mode: str, event: Any) -> Any:
    if isinstance(event, tuple) and len(event) == 2 and event[0] == mode:
        return event[1]
    return event


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

# print("—— 裸 LLM（不会调 get_weather）：", end="")
# for chunk in llm.stream("请查询南京当前天气，用工具查到的结果简要回答。"):
#     print(chunk.content, end="", flush=True)
# print()

# print("—— Agent（会按需调工具）：")
# for chunk in agent.stream(_user_weather, stream_mode="updates"):
#     print(chunk, end="", flush=True)
#     print()

# ---------- 示例：默认只跑 ①；②～⑤ 请取消注释分别试（每次都会完整跑一遍 Agent）----------
print("=== ① updates（print_updates_str_mode）===")
for ev in agent.stream(_user_weather, stream_mode="updates"):
    print_updates_str_mode(ev)
    print("  ---")

# print("\n=== ② messages（print_messages_str_mode）===")
# for ev in agent.stream(_user_weather, stream_mode="messages"):
#     print_messages_str_mode(ev)
# print()

# print("\n=== ③ values（print_values_str_mode）===")
# for ev in agent.stream(_user_weather, stream_mode="values"):
#     print_values_str_mode(ev)
#     print("  ---")

# print("\n=== ④ custom（print_custom_str_mode）===")
# for ev in agent.stream(_user_weather, stream_mode="custom"):
#     print_custom_str_mode(ev)

# print("\n=== ⑤ debug（print_debug_str_mode）===")
# for ev in agent.stream(_user_weather, stream_mode="debug"):
#     print_debug_str_mode(ev)
#     print("  ---")

# # StrOutputParser 用于「线性链」如 prompt | llm | StrOutputParser()，把单条模型输出转成 str；
# # Agent 图流式输出是多节点 state 更新，需像上面这样解析 dict，或下面这样只要最终一句。
# # 下列 invoke 与上方 stream 会各跑一遍 Agent，生产环境请二选一以免重复计费。
# print("—— 仅最终回复（invoke + 最后一条 AIMessage）：")
# _final = agent.invoke(_user_weather)
# _last = _final["messages"][-1]
# if isinstance(_last, AIMessage) and _last.content:
#     print(_last.content)
# else:
#     print(_last)

# # 流式用 stream / astream；invoke 只返回最终 state，不按 token 推送。
# # stream_mode="messages" 时，常见每条 event 为二元组：(消息对象, 元数据 dict)。
# # 元数据里 langgraph_node 标明来自哪个节点："model"=聊天模型流式块，"tools"=工具节点写回的整段 ToolMessage。
# print("—— Agent stream_mode=\"messages\"（从 event 取 msg.content 打印）：")
# for event in agent.stream(_user_weather, stream_mode="messages"):
#     if isinstance(event, tuple) and len(event) == 2 and isinstance(event[1], dict):
#         msg, meta = event[0], event[1]
#     else:
#         msg, meta = event, {}

#     node = meta.get("langgraph_node", "")

#     # 模型流：每条是 AIMessageChunk，真正要打的字在 .content（可能为空字符串，工具调用前后会穿插空块）
#     if node == "model" and isinstance(msg, AIMessageChunk) and msg.content:
#         print(msg.content, end="", flush=True)

#     # 工具节点：图里等工具函数跑完才有一条 ToolMessage，messages 流里不会拆成多段 token（与 LLM 不同）。
#     # 若要「打字机」观感，只能对 msg.content 在本地逐字打印；需要停顿可加 time.sleep（演示用）。
#     elif node == "tools" and isinstance(msg, ToolMessage):
#         print(f"\n[工具 {msg.name}] ", end="", flush=True)
#         for ch in msg.content:
#             print(ch, end="", flush=True)
#         print("\n", flush=True)
# print()
