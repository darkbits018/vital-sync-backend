import os

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.schemas.chat_message import ChatMessage, ChatMessageCreate
from app.db.session import get_db
from app.services.firebase_auth import get_current_user
from app.services.chat_service import send_message, get_chat_history

router = APIRouter()


@router.get("/history", response_model=list[ChatMessage])
async def read_chat_history(
        skip: int = 0,
        limit: int = 100,
        db: Session = Depends(get_db),
        current_user: dict = Depends(get_current_user)
):
    return get_chat_history(db, current_user["uid"], skip, limit)


@router.post("/", response_model=ChatMessage, status_code=status.HTTP_201_CREATED)
async def post_message(
        message: ChatMessageCreate,
        ai_model: str = "gemini",
        db: Session = Depends(get_db),
        current_user: dict = Depends(get_current_user)
):
    return send_message(db, message, current_user["uid"], ai_model, os.getenv("AI_API_KEY"))
