from fastapi import FastAPI
from threading import Thread
from app.api.chat import router as chat_router
from app.api.websocket import router as websocket_router
from app.core.ai_worker import start_ai_worker


app = FastAPI()
app.include_router(chat_router)
app.include_router(websocket_router)

"""
Run the AI worker in a separate thread, to consume messages from Redis
"""

@app.on_event("startup")
def startup():
    Thread(target=start_ai_worker, daemon=True).start()