from pathlib import Path

# `src` 目录：相对路径默认相对这里解析，不依赖运行时的当前工作目录
_SRC_ROOT = Path(__file__).resolve().parent.parent


def resolve_raw_path(raw_file_path: str | Path) -> Path:
    """
    解析 raw_file_path 的绝对路径，并折叠 . / .. 等冗余段。
    """
    p = Path(raw_file_path)
    base = p if p.is_absolute() else _SRC_ROOT / p
    return base.resolve()

if __name__ == "__main__":
    raw_file_path = r"../data/AI/大模型（LLM）开发.md"
    path = resolve_raw_path(raw_file_path)
    print(path)