import os
from typing import List, Optional, Tuple

import numpy as np
from dotenv import load_dotenv
from openai import OpenAI


class StudioOpenAI:
    """
    学习用：环境与 OpenAI 兼容客户端（仅类方法，无模块级函数）。
    千问百炼 DashScope、DeepSeek 等均可通过 .env 切换。
    """

    @classmethod
    def load_env(cls) -> None:
        load_dotenv()

    @classmethod
    def default_base_url(cls) -> str:
        cls.load_env()
        env = os.getenv("BASE_URL")
        if env:
            return env.rstrip("/")
        if os.getenv("DASHSCOPE_API_KEY"):
            return "https://dashscope.aliyuncs.com/compatible-mode/v1"
        return "https://api.deepseek.com"

    @classmethod
    def infer_base_url(cls, client: OpenAI) -> str:
        bu = client.base_url
        return str(bu).rstrip("/") if bu else ""

    @classmethod
    def default_chat_model(cls, base_url: str) -> str:
        cls.load_env()
        env = os.getenv("CHAT_MODEL")
        if env:
            return env
        return "qwen-turbo" if "dashscope" in base_url else "deepseek-chat"

    @classmethod
    def create_client(cls) -> OpenAI:
        cls.load_env()
        api_key = os.getenv("DASHSCOPE_API_KEY") or os.getenv("DEEPSEEK_API_KEY")
        if not api_key or api_key == "你的Key":
            raise ValueError(
                "请在项目根目录 .env 中设置 DASHSCOPE_API_KEY（千问）或 DEEPSEEK_API_KEY（DeepSeek）"
            )
        return OpenAI(api_key=api_key, base_url=cls.default_base_url())


class CosineSimilarityRetriever:
    """
    学习用：向量化 + 余弦相似度，从多条文本里挑出与 query 最相关的一条。
    查询与文档必须用本类的 embed，维度才一致。
    """

    def __init__(
        self,
        client: Optional[OpenAI] = None,
        embedding_model: str = "text-embedding-v3",
    ):
        self.client = client or StudioOpenAI.create_client()
        self.embedding_model = embedding_model

    def embed(self, text: str) -> np.ndarray:
        text = text.replace("\n", " ")
        response = self.client.embeddings.create(
            model=self.embedding_model,
            input=text,
            encoding_format="float",
        )
        return np.array(response.data[0].embedding)

    @classmethod
    def cosine_similarity(cls, vec_a: np.ndarray, vec_b: np.ndarray) -> float:
        denom = float(np.linalg.norm(vec_a) * np.linalg.norm(vec_b) + 1e-10)
        return float(np.dot(vec_a, vec_b) / denom)

    def retrieve(
        self, query: str, documents: List[str]
    ) -> Tuple[str, List[float]]:
        q_emb = self.embed(query)
        scores: List[float] = []
        best_i = 0
        best_s = -1.0
        for i, doc in enumerate(documents):
            d_emb = self.embed(doc)
            s = self.cosine_similarity(q_emb, d_emb)
            scores.append(s)
            if s > best_s:
                best_s = s
                best_i = i
        return documents[best_i], scores


class QianwenChat:
    """
    学习用：通过 OpenAI 兼容接口调用通义千问（或其它兼容服务商）的对话能力。
    """

    def __init__(self, client: Optional[OpenAI] = None, model: Optional[str] = None):
        self.client = client or StudioOpenAI.create_client()
        if model is not None:
            self.model = model
        else:
            base = StudioOpenAI.infer_base_url(self.client)
            self.model = StudioOpenAI.default_chat_model(base)

    def complete(self, user_text: str) -> str:
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": user_text}],
        )
        msg = response.choices[0].message
        return (msg.content or "").strip()
