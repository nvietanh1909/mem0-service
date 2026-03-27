import logging

from fastapi import FastAPI

from app.routers.v1 import chat, health, memories

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)

app = FastAPI(
    title="Mem0 Memory Service",
    description="RESTful API service for AI memory management powered by Mem0",
    version="1.0.0",
)

v1_prefix = "/api/v1"

app.include_router(health.router, prefix=v1_prefix)
app.include_router(memories.router, prefix=v1_prefix)
app.include_router(chat.router, prefix=v1_prefix)
