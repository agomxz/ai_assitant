# AI Assistant

This project is a simplle AI assistant that uses Redis Streams in order to implement a pub/sub messaging system

## Tech Stack
- FastAPI
- Redis
- Python


## How to run
1. docker compose up -d
2. uvicorn app.main:app --reload
3. wscat -c ws://localhost:8000/ws/123 


## Description
Client
  ↓
FastAPI (/chat/send)
  ↓
Redis Stream (chat:incoming)
  ↓
AI Worker (consumer group)
  ↓
Redis Stream (chat:outgoing)
  ↓
API / WebSocket


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