from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.tools import tool
from pathlib import Path
import re
from utils.resolve_path import resolve_raw_path


def simple_cleaner(text):
    """
    清洗文本，去除 Markdown 链接和图片代码，去除十六进制乱码或过长的无意义字符串，合并过多的换行符，让文本更紧凑
    Args:
        text: 待清洗的文本
    Returns:
        str: 清洗后的文本
    """
    # 1. 去除 Markdown 链接和图片代码 (e.g., [text](url) 或 ![alt](url))
    text = re.sub(r"!\[.*?\]\(.*?\)", "", text)
    text = re.sub(r"\[.*?\]\(.*?\)", "", text)

    # 2. 去除十六进制乱码或过长的无意义字符串
    text = re.sub(r"[a-fA-F0-9]{32,}", "", text)

    # 3. 合并过多的换行符，让文本更紧凑
    text = re.sub(r"\n+", "\n", text)

    return text.strip()


def _split_markdown(raw_file_path: str | Path):
    """
    读取 raw_file_path 下的 Markdown，清洗后按块切分。(不用注释掉 @tool 装饰器)
    若为相对路径，则相对于本包下的 src 目录（与 data/ 同级），不随终端 cwd 变化。
    Args:
        raw_file_path: 待读取的 Markdown 文件路径
    Returns:
        list[str]: 清洗后的文本列表
    """
    path = resolve_raw_path(raw_file_path)
    with open(path, "r", encoding="utf-8") as f:
        raw_messy_markdown = f.read()

    # 使用清洗后的文本
    clean_text = simple_cleaner(raw_messy_markdown)

    # 针对杂乱文档，使用递归切分，尽量保持段落完整
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,  # 每个块的大小
        chunk_overlap=200,  # 块与块之间的重叠，防止知识点被从中间劈开
        separators=["\n\n", "\n", "。", "！", "？", " ", ""],
    )

    chunks = text_splitter.split_text(clean_text)
    return chunks


@tool
def split_markdown(raw_file_path: str | Path):
    """
    读取 raw_file_path 下的 Markdown，清洗后按块切分。
    若为相对路径，则相对于本包下的 src 目录（与 data/ 同级），不随终端 cwd 变化。
    Args:
        raw_file_path: 待读取的 Markdown 文件路径
    Returns:
        list[str]: 清洗后的文本列表
    """
    return _split_markdown(raw_file_path)


if __name__ == "__main__":
    raw_file_path = r"../data/AI/大模型（LLM）开发.md"
    chunks = _split_markdown(raw_file_path)
    print(chunks)
