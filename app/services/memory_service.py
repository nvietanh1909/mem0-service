import logging
import json
from mem0 import Memory

from app.config import get_settings

logger = logging.getLogger(__name__)


class MemoryService:
    def __init__(self):
        settings = get_settings()
        mem0_config = settings.get_mem0_config()
        self._memory = Memory.from_config(mem0_config)

    def add(self, messages: list[dict], user_id: str, agent_id: str = None,
            run_id: str = None, metadata: dict = None) -> dict:
        kwargs = {"user_id": user_id}
        if agent_id:
            kwargs["agent_id"] = agent_id
        if run_id:
            kwargs["run_id"] = run_id
        if metadata:
            kwargs["metadata"] = metadata

        result = self._memory.add(messages, **kwargs)
        return result

    def search(self, query: str, user_id: str, agent_id: str = None,
               limit: int = 5) -> dict:
        kwargs = {"user_id": user_id, "limit": limit}
        if agent_id:
            kwargs["agent_id"] = agent_id

        result = self._memory.search(query=query, **kwargs)
        return result

    def get_all(self, user_id: str, agent_id: str = None) -> list:
        kwargs = {"user_id": user_id}
        if agent_id:
            kwargs["agent_id"] = agent_id

        result = self._memory.get_all(**kwargs)
        return result

    def get(self, memory_id: str) -> dict:
        result = self._memory.get(memory_id)
        return result

    def update(self, memory_id: str, data: str) -> dict:
        result = self._memory.update(memory_id, data=data)
        return result

    def delete(self, memory_id: str) -> dict:
        self._memory.delete(memory_id)
        return {"id": memory_id, "deleted": True}

    def delete_all(self, user_id: str, agent_id: str = None) -> dict:
        kwargs = {"user_id": user_id}
        if agent_id:
            kwargs["agent_id"] = agent_id

        self._memory.delete_all(**kwargs)
        return {"user_id": user_id, "agent_id": agent_id, "deleted": True}

    def history(self, memory_id: str) -> list:
        result = self._memory.history(memory_id)
        return result


_memory_service: MemoryService | None = None


def get_memory_service() -> MemoryService:
    global _memory_service
    if _memory_service is None:
        logger.info("Initializing MemoryService...")
        _memory_service = MemoryService()
        logger.info("MemoryService initialized successfully")
    return _memory_service
