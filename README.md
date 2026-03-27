# Self-Hosted Mem0 Memory Service

A self-hosted production-ready memory built with FastAPI and Mem0. This service provides long-term, personalized memory for AI agents, integrating with your own Qdrant instance and choice of LLMs.

## Features

- Long-term memory management for multiple users and agents.
- Semantic search and retrieval using Qdrant vector database.
- Automated fact extraction from conversation history.
- Built-in chat interface with integrated memory context.
- API Key authentication and secure configuration management.

## Tech Stack

- Framework: FastAPI
- Core Engine: Mem0 (mem0ai)
- Vector Store: Qdrant
- History Tracking: SQLite
- Containerization: Docker & Docker Compose

## Prerequisites

- Docker and Docker Compose installed on your system.
- An OpenAI-compatible LLM endpoint (e.g., Qwen, GPT-4).

## Configuration

1. Copy `.env.example` to `.env`:
   ```bash
   cp .env.example .env
   ```
2. Configure your LLM and API keys in `.env`:
   - `LLM_BASE_URL`: Your LLM provider endpoint.
   - `LLM_API_KEY`: Your LLM API key.
   - `API_KEY`: The authentication key for this service (default: mem0@).

## Deployment

Build and start the services in detached mode:
```bash
docker-compose up -d --build
```

To stop the services:
```bash
docker-compose down
```

To reset all data (wipes Qdrant and SQLite volumes):
```bash
docker-compose down -v
```

## API Testing

### Health Check
```bash
curl -s http://localhost:8000/api/v1/health
```

### Chat with Memory
```bash
curl -s -X POST "http://localhost:8000/api/v1/chat" \
     -H "mem0: mem0@" \
     -H "Content-Type: application/json" \
     -d '{
       "message": "My name is Tuan and I love Python.",
       "user_id": "user_01"
     }'
```

### Search Memories
```bash
curl -s -G "http://localhost:8000/api/v1/memories/search" \
     -H "mem0: mem0@" \
     --data-urlencode "query=What is my name?" \
     --data-urlencode "user_id=user_01"
```

## Project Structure

- /app/routers: API endpoint definitions.
- /app/services: Core logic for memory and chat orchestration.
- /app/schemas: Pydantic models for request/response validation.
- /config.yaml: Mem0 internal configuration (embedder, vector store).
- /docker-compose.yml: Infrastructure orchestration.
