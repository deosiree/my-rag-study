from IPython.display import display, Markdown
import os
import re

def _clean_mermaid_source(raw_code: str) -> str:
    """
    内部工具函数：清洗 LangGraph 生成的原始 Mermaid 文本。
    解决 config 报错、HTML 实体报错以及不必要的标签。
    """
    # 1. 移除开头的 ---config--- 块 (非贪婪匹配直到第二个 ---)
    clean_code = re.sub(r'^---.*?---', '', raw_code, flags=re.DOTALL).strip()
    
    # 2. 替换 HTML 转义字符（这是导致 'got SEMI' 报错的主因）
    clean_code = clean_code.replace('&nbsp;', ' ')
    
    # 3. 移除可能干扰渲染的 HTML 标签
    clean_code = clean_code.replace('<p>', '').replace('</p>', '')
    
    # 4. 确保以标准 graph 开头 (防止多余的换行)
    clean_code = clean_code.lstrip()
    
    return clean_code

def visualize_graph(app, filename="ipython_output.md", display_inline=True):
    """
    可视化并持久化图结构
    - 自动创建文件和必要的文件夹
    - 默认 UTF-8 编码避免中文乱码
    1. 生成 Mermaid 源码
    2. 在 Jupyter 中渲染预览
    3. 自动写入到指定的本地 Markdown 文件
    """
    try:
        # 1. 获取 Mermaid 源码
        mermaid_code = app.get_graph().draw_mermaid()
        markdown_text = f"### Graph Flow\n\n```mermaid\n{mermaid_code}\n```"

        # 2. 清洗 Mermaid 源码
        cleaned_mermaid = _clean_mermaid_source(mermaid_code)
        cleaned_text = f"### Graph Flow\n\n```mermaid\n{cleaned_mermaid}\n```"

        
        # 4. 确保目录存在 (处理 'outputs/graph.md' 这种情况)
        dir_name = os.path.dirname(filename)
        if dir_name and not os.path.exists(dir_name):
            os.makedirs(dir_name)
            print(f"📁 已创建目录: {dir_name}")

        # 5. 写入文件 (模式 "w" 会自动新建文件)
        with open(filename, "w", encoding="utf-8") as f:
            f.write(cleaned_text)
            print(f"📄 已写入文件: {filename}")
        
        # 6. Jupyter 内部渲染
        if display_inline:
            display(Markdown(markdown_text))
            
        return cleaned_text

    except Exception as e:
        error_msg = f"可视化失败: {str(e)}"
        print(error_msg)
        return error_msg

# --- 使用方式 ---
# 直接运行即可，无需手动 touch ipython_output.md
# md_code = visualize_graph(app, filename="ipython_output.md")