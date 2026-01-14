from pydantic import BaseModel
from typing import Optional


class SendMessageResponse(BaseModel):
    status: str
    session_id: str
    message_id: str


class ErrorResponse(BaseModel):
    status: str
    detail: str
