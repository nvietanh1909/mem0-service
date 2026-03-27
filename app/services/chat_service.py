import logging
import re

from openai import OpenAI

from app.config import get_settings
from app.services.memory_service import get_memory_service

logger = logging.getLogger(__name__)

DEFAULT_SYSTEM_PROMPT = (
    "You are a helpful and friendly AI assistant. "
    "Use the provided user memories to personalize your responses. "
    "Always respond in the same language as the user's message. "
    "Do not include your thinking process in the response."
)


class ChatService:
    def __init__(self):
        settings = get_settings()
        self._client = OpenAI(
            base_url=settings.llm_base_url,
            api_key=settings.llm_api_key,
        )
        self._model = settings.llm_model_name
        self._memory_service = get_memory_service()

    def chat(
        self,
        message: str,
        user_id: str,
        agent_id: str = None,
        system_prompt: str = None,
        memory_limit: int = 5,
    ) -> dict:
        relevant_memories = self._memory_service.search(
            query=message,
            user_id=user_id,
            agent_id=agent_id,
            limit=memory_limit,
        )
        memories_list = relevant_memories.get("results", [])
        memories_str = "\n".join(
            f"- {entry['memory']}" for entry in memories_list
        )

        base_prompt = system_prompt or DEFAULT_SYSTEM_PROMPT
        if memories_str:
            full_system_prompt = (
                f"{base_prompt}\n\nUser Memories:\n{memories_str}"
            )
        else:
            full_system_prompt = base_prompt

        messages = [
            {"role": "system", "content": full_system_prompt},
            {"role": "user", "content": message},
        ]

        completion = self._client.chat.completions.create(
            model=self._model,
            messages=messages,
            temperature=0.7,
            max_tokens=2000,
        )
        assistant_response = completion.choices[0].message.content

        assistant_response = re.sub(r"<think>.*?</think>", "", assistant_response, flags=re.DOTALL)
        assistant_response = re.sub(r"Thinking Process:.*?\n\n", "", assistant_response, flags=re.DOTALL)
        assistant_response = assistant_response.strip()

        conversation = [
            {"role": "user", "content": message},
            {"role": "assistant", "content": assistant_response},
        ]
        add_result = self._memory_service.add(
            messages=conversation,
            user_id=user_id,
            agent_id=agent_id,
        )
        memories_created = add_result.get("results", [])

        return {
            "response": assistant_response,
            "memories_used": memories_list,
            "memories_created": memories_created,
        }


_chat_service: ChatService | None = None


def get_chat_service() -> ChatService:
    global _chat_service
    if _chat_service is None:
        logger.info("Initializing ChatService...")
        _chat_service = ChatService()
        logger.info("ChatService initialized successfully")
    return _chat_service
