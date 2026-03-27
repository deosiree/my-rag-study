from typing import Literal

# 1. 定义心情决定函数
# Literal 确保了返回值只能是这两个固定选项
def decide_mood(user_text: str) -> Literal["happy", "sad"]:
    """
    这是一个简单的“逻辑边”判断函数。
    它根据用户的输入内容，决定流程走向。
    """
    positive_words = ["好", "开心", "棒", "赢", "顺利"]
    
    # 简单的逻辑判断：如果输入包含正面词汇，返回 happy
    if any(word in user_text for word in positive_words):
        return "happy"
    else:
        return "sad"

# 2. 用户参与环节
print("--- AI 心情状态机 ---")
user_input = input("请描述你今天过得怎么样：")

# 调用逻辑边
result = decide_mood(user_input)

# 3. 根据 Literal 的返回值走向不同的分支（条件边应用）
if result == "happy":
    print("✨ 检测到正向情绪！正在为您播放欢快的音乐...")
elif result == "sad":
    print("💙 检测到负向情绪。正在为您准备热可可和安慰话语...")

# 故意写错测试（在编辑器中，下面这行会报错，因为 "angry" 不在 Literal 中）
# wrong_test: Literal["happy", "sad"] = "angry"