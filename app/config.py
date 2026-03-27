import os
import logging
from pathlib import Path
from functools import lru_cache

import yaml
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent
logger = logging.getLogger(__name__)


def load_yaml_config(path: str = None) -> dict:
    if path is None:
        path = BASE_DIR / "config.yaml"
    with open(path, "r") as f:
        return yaml.safe_load(f)


class Settings:
    def __init__(self):
        self._yaml = load_yaml_config()
        logger.info(f"DEBUG: Loaded YAML keys: {list(self._yaml.keys())}")
        self._app = self._yaml.get("app", {})
        self._mem0 = self._yaml.get("mem0", {})

    @property
    def app_host(self) -> str:
        return self._app.get("host", "0.0.0.0")

    @property
    def app_port(self) -> int:
        return self._app.get("port", 8000)

    @property
    def api_key(self) -> str:
        return os.getenv("API_KEY", "mem0@")

    @property
    def api_key_header(self) -> str:
        return os.getenv("API_KEY_HEADER", "mem0")

    @property
    def llm_base_url(self) -> str:
        return os.getenv("LLM_BASE_URL", "")

    @property
    def llm_api_key(self) -> str:
        return os.getenv("LLM_API_KEY", "")

    @property
    def llm_model_name(self) -> str:
        return os.getenv("LLM_MODEL_NAME", "")

    def get_mem0_config(self) -> dict:
        llm_cfg = self._mem0.get("llm", {})
        embedder_cfg = self._mem0.get("embedder", {})
        vector_store_cfg = self._mem0.get("vector_store", {})

        return {
            "llm": {
                "provider": llm_cfg.get("provider", "openai"),
                "config": {
                    "model": self.llm_model_name,
                    "openai_base_url": self.llm_base_url,
                    "api_key": self.llm_api_key,
                    "temperature": llm_cfg.get("temperature", 0.1),
                    "max_tokens": llm_cfg.get("max_tokens", 2000),
                },
            },
            "embedder": {
                "provider": embedder_cfg.get("provider", "huggingface"),
                "config": {
                    "model": embedder_cfg.get("model", "multi-qa-MiniLM-L6-cos-v1"),
                    "embedding_dims": 384,
                },
            },
            "vector_store": {
                "provider": vector_store_cfg.get("provider", "qdrant"),
                "config": {
                    "collection_name": vector_store_cfg.get("collection_name", "mem0_memories"),
                    "host": os.getenv("QDRANT_HOST", vector_store_cfg.get("host", "localhost")),
                    "port": int(os.getenv("QDRANT_PORT", str(vector_store_cfg.get("port", 6333)))),
                    "embedding_model_dims": embedder_cfg.get("embedding_model_dims", 384),
                },
            },
        }


@lru_cache()
def get_settings() -> Settings:
    return Settings()
