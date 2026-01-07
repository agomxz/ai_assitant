from fastapi import FastAPI
from app.api.chat import router
from app.core.ai_worker import start_ai_worker

app = FastAPI()
app.include_router(router)

@app.on_event("startup")
async def startup():
    start_ai_worker()
