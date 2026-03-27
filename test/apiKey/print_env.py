import os
from dotenv import load_dotenv
load_dotenv() # 这一行会把 .env 的值加载到 os.environ

api_key = os.environ.get("CUSTOM_API_KEY")
base_url = os.environ.get("CUSTOM_BASE_URL")
model = os.environ.get("CUSTOM_MODEL_NAME")
print(api_key, base_url, model)