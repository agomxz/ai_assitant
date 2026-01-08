# AI Assistant


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


## How to run
docker compose up -d
uvicorn app.main:app --reload


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

