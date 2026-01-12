# AI Assistant

This project is a simplle AI assistant that uses Redis Streams in order to implement a pub/sub messaging system
For answer the chat uses Ollama with OpenAI model (gpt-oss)
Expose a websocket to consume the messages of the AI Agent

## Tech Stack
- FastAPI
- Redis
- Python
- Docker
- Ollama


## How to run
1. docker compose up -d
2. ollama run gpt-oss
2. uvicorn app.main:app --reload
3. wscat -c ws://localhost:8000/ws/123 


## Architecture Overview

```mermaid
erDiagram
flowchart TB
    Client[Client] 
        --> API[FastAPI<br/>(/chat/send)]
    API 
        --> RedisIn[Redis Stream<br/>(chat:incoming)]
    RedisIn 
        --> Worker[AI Worker]
    Worker 
        --> RedisOut[Redis Stream<br/>(chat:outgoing)]
    RedisOut 
        --> WS[WebSocket]
```


## Repo Structure
ai-assistant/
├── app/
│   ├── main.py                # FastAPI entrypoint
│   ├── config.py              # env vars & settings
│   │
│   ├── api/
│   │   ├── __init__.py
│   │   └── chat.py            # send / receive endpoints
│   │
│   ├── core/
│   │   ├── __init__.py
│   │   ├── event_bus.py       # publish / subscribe abstraction
│   │   └── ai_worker.py       # mocked or real AI listener
│   │
│   ├── models/
│   │   ├── __init__.py
│   │   └── chat.py            # Pydantic models
│   │
│   ├── services/
│   │   ├── __init__.py
│   │   └── ai_service.py      # AI logic (mocked / OpenAI / Bedrock)
│   │
│   └── utils/
│       ├── __init__.py
│       └── logger.py
│
├── tests/
│   └── test_chat.py
│
├── requirements.txt
├── .env
├── .gitignore
└── README.md