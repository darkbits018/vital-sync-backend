from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class NotificationBase(BaseModel):
    title: str
    body: str
    created_at: Optional[datetime] = None


class NotificationCreate(NotificationBase):
    pass


class Notification(NotificationBase):
    id: str
    user_id: str

    class Config:
        from_attributes = True
