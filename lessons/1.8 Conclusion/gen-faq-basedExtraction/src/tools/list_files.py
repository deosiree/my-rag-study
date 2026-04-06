from langchain_core.tools import tool
import os
from utils.resolve_path import resolve_raw_path


def _list_files(directory_path: str):
    """
    获取指定文件夹下的所有文件列表。（内部函数，因为 @tool 后就不能当普通函数使用了）
    Args:
        directory_path: 文件夹路径
    Returns:
        list: 文件列表
    """
    dir_path = resolve_raw_path(directory_path)
    result = []
    for file in os.listdir(dir_path):
        if os.path.isfile(os.path.join(dir_path, file)):
            result.append(file)
        elif os.path.isdir(os.path.join(dir_path, file)):
            result.extend(_list_files(os.path.join(dir_path, file)))
    return result

@tool
def list_files(directory_path: str):
    """
    获取指定文件夹下的所有文件列表。
    Args:
        directory_path: 文件夹路径
    Returns:
        list: 文件列表
    """
    return _list_files(directory_path)

if __name__ == "__main__":
    print(_list_files(r"../data/AI/LangGraph/models模型类"))