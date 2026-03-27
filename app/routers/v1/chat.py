import logging

from fastapi import APIRouter, Depends, HTTPException, status

from app.dependencies import verify_api_key
from app.schemas.chat import ChatRequest, ChatResponse
from app.services.chat_service import get_chat_service

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/chat",
    tags=["chat"],
    dependencies=[Depends(verify_api_key)],
)


@router.post("", response_model=ChatResponse)
async def chat(request: ChatRequest):
    try:
        service = get_chat_service()
        result = service.chat(
            message=request.message,
            user_id=request.user_id,
            agent_id=request.agent_id,
            system_prompt=request.system_prompt,
            memory_limit=request.memory_limit,
        )
        return ChatResponse(
            response=result["response"],
            memories_used=result["memories_used"],
            memories_created=result["memories_created"],
        )
    except Exception as e:
        logger.exception("Failed to process chat")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )
