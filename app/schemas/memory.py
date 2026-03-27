from pydantic import BaseModel, Field


class AddMemoryRequest(BaseModel):
    messages: list[dict] = Field(..., min_length=1)
    user_id: str
    agent_id: str | None = None
    run_id: str | None = None
    metadata: dict | None = None


class SearchMemoryRequest(BaseModel):
    query: str
    user_id: str
    agent_id: str | None = None
    limit: int = Field(default=5, ge=1, le=50)


class UpdateMemoryRequest(BaseModel):
    data: str


class DeleteAllRequest(BaseModel):
    user_id: str
    agent_id: str | None = None


class MemoryItem(BaseModel):
    id: str
    memory: str
    user_id: str | None = None
    agent_id: str | None = None
    hash: str | None = None
    metadata: dict | None = None
    created_at: str | None = None
    updated_at: str | None = None


class AddMemoryResponse(BaseModel):
    status: str = "ok"
    results: list[dict]


class SearchMemoryResponse(BaseModel):
    status: str = "ok"
    results: list[dict]


class MemoryListResponse(BaseModel):
    status: str = "ok"
    memories: list[dict]
    total: int


class MemoryDetailResponse(BaseModel):
    status: str = "ok"
    memory: dict


class DeleteResponse(BaseModel):
    status: str = "ok"
    message: str


class HistoryResponse(BaseModel):
    status: str = "ok"
    history: list[dict]


class ErrorResponse(BaseModel):
    status: str = "error"
    detail: str
