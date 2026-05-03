import asyncio
from browser_use_sdk.v3 import AsyncBrowserUse


# 定义一个异步主函数
async def main():
    # 创建一个AsyncBrowserUse类的实例，用于异步浏览器操作
    client = AsyncBrowserUse(api_key="bu_ZNzgwhTqJHuRuGFje6zq4a-uL3IY6LH6cnmTZ9LCc_o")
    # 调用client的run方法，执行获取Hacker News今日前20个帖子及其得分的任务
    # run方法是异步的，使用await关键字等待其完成
    result = await client.run(
        "List the top 20 posts on Hacker News today with their points", model="bu-mini"
    )
    # 打印执行结果中的输出内容
    print(result.output)


asyncio.run(main())
