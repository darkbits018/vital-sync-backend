from sqlalchemy.orm import Session
from app.models.chat_message import ChatMessage as ChatMessageModel
from app.schemas.chat_message import ChatMessage, ChatMessageCreate
from app.services.ai_integrations import AIIntegrationFactory


def get_chat_history(db: Session, user_id: str, skip: int = 0, limit: int = 100) -> list[ChatMessage]:
    return db.query(ChatMessageModel).filter(ChatMessageModel.user_id == user_id).offset(skip).limit(limit).all()


def send_message(db: Session, message: ChatMessageCreate, user_id: str, ai_model: str = "gemini",
                 ai_api_key: str = None) -> ChatMessage:
    db_message = ChatMessageModel(**message.dict(), user_id=user_id)
    db.add(db_message)
    db.commit()
    db.refresh(db_message)

    # Get AI response
    ai_service = AIIntegrationFactory.get_service(ai_model, ai_api_key)
    ai_response = ai_service.generate_response(message.content)

    # Save AI response
    db_ai_message = ChatMessageModel(
        content=ai_response,
        role="assistant",
        user_id=user_id
    )
    db.add(db_ai_message)
    db.commit()
    db.refresh(db_ai_message)

    return db_ai_message
