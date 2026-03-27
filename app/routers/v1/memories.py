import logging

from fastapi import APIRouter, Depends, HTTPException, Query, status

from app.dependencies import verify_api_key
from app.schemas.memory import (
    AddMemoryRequest,
    AddMemoryResponse,
    DeleteAllRequest,
    DeleteResponse,
    HistoryResponse,
    MemoryDetailResponse,
    MemoryListResponse,
    SearchMemoryResponse,
    UpdateMemoryRequest,
)
from app.services.memory_service import get_memory_service

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/memories",
    tags=["memories"],
    dependencies=[Depends(verify_api_key)],
)


@router.post("", response_model=AddMemoryResponse)
async def add_memory(request: AddMemoryRequest):
    try:
        service = get_memory_service()
        result = service.add(
            messages=request.messages,
            user_id=request.user_id,
            agent_id=request.agent_id,
            run_id=request.run_id,
            metadata=request.metadata,
        )
        return AddMemoryResponse(results=result.get("results", []))
    except Exception as e:
        logger.exception("Failed to add memory")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )


@router.get("/search", response_model=SearchMemoryResponse)
async def search_memories(
    query: str = Query(...),
    user_id: str = Query(...),
    agent_id: str = Query(default=None),
    limit: int = Query(default=5, ge=1, le=50),
):
    try:
        service = get_memory_service()
        result = service.search(
            query=query,
            user_id=user_id,
            agent_id=agent_id,
            limit=limit,
        )
        return SearchMemoryResponse(results=result.get("results", []))
    except Exception as e:
        logger.exception("Failed to search memories")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )


@router.get("", response_model=MemoryListResponse)
async def get_all_memories(
    user_id: str = Query(...),
    agent_id: str = Query(default=None),
):
    try:
        service = get_memory_service()
        result = service.get_all(user_id=user_id, agent_id=agent_id)
        memories = result.get("results", []) if isinstance(result, dict) else result
        return MemoryListResponse(memories=memories, total=len(memories))
    except Exception as e:
        logger.exception("Failed to get memories")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )


@router.get("/{memory_id}", response_model=MemoryDetailResponse)
async def get_memory(memory_id: str):
    try:
        service = get_memory_service()
        result = service.get(memory_id=memory_id)
        return MemoryDetailResponse(memory=result)
    except Exception as e:
        logger.exception("Failed to get memory")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )


@router.put("/{memory_id}", response_model=MemoryDetailResponse)
async def update_memory(memory_id: str, request: UpdateMemoryRequest):
    try:
        service = get_memory_service()
        result = service.update(memory_id=memory_id, data=request.data)
        return MemoryDetailResponse(memory=result)
    except Exception as e:
        logger.exception("Failed to update memory")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )


@router.delete("/{memory_id}", response_model=DeleteResponse)
async def delete_memory(memory_id: str):
    try:
        service = get_memory_service()
        service.delete(memory_id=memory_id)
        return DeleteResponse(message=f"Memory {memory_id} deleted successfully")
    except Exception as e:
        logger.exception("Failed to delete memory")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )


@router.delete("", response_model=DeleteResponse)
async def delete_all_memories(request: DeleteAllRequest):
    try:
        service = get_memory_service()
        service.delete_all(user_id=request.user_id, agent_id=request.agent_id)
        return DeleteResponse(
            message=f"All memories deleted for user_id={request.user_id}"
        )
    except Exception as e:
        logger.exception("Failed to delete all memories")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )


@router.get("/{memory_id}/history", response_model=HistoryResponse)
async def get_memory_history(memory_id: str):
    try:
        service = get_memory_service()
        result = service.history(memory_id=memory_id)
        return HistoryResponse(history=result)
    except Exception as e:
        logger.exception("Failed to get memory history")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )
