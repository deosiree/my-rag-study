import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()  # 这一行会把 .env 的值加载到 os.environ
# # 优先读取当前目录下 .env，避免工作目录变化导致加载失败。
# _ENV_PATH = Path(__file__).resolve().parent / ".env"
# load_dotenv(dotenv_path=_ENV_PATH)

# OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
# OPENAI_BASE_URL = os.getenv("OPENAI_BASE_URL")
# OPENAI_MODEL = os.getenv("OPENAI_MODEL")
api_key = os.environ.get("CUSTOM_API_KEY")
base_url = os.environ.get("CUSTOM_BASE_URL")
model = os.environ.get("CUSTOM_MODEL_NAME")
print(api_key, base_url, model)