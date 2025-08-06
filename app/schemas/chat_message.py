from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class ChatMessageBase(BaseModel):
    role: str
    content: str
    timestamp: datetime


class ChatMessageCreate(ChatMessageBase):
    user_id: str


class ChatMessage(ChatMessageBase):
    id: str
    user_id: str

    class Config:
        from_attributes = True
