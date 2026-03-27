from fastapi import Security, HTTPException, status
from fastapi.security import APIKeyHeader

from app.config import get_settings

settings = get_settings()
api_key_header = APIKeyHeader(name=settings.api_key_header, auto_error=False)


async def verify_api_key(api_key: str = Security(api_key_header)):
    if not api_key or api_key != settings.api_key:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid or missing API Key",
        )
    return api_key
