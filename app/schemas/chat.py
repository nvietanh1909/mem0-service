from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1)
    user_id: str
    agent_id: str | None = None
    system_prompt: str | None = None
    memory_limit: int = Field(default=5, ge=1, le=20)


class ChatResponse(BaseModel):
    status: str = "ok"
    response: str
    memories_used: list[dict] = []
    memories_created: list[dict] = []
