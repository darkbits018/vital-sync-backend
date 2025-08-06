from socketio import AsyncServer
from app.services.chat_service import send_message
from app.db.session import get_db
from app.schemas.chat_message import ChatMessageCreate
from app.services.firebase_auth import get_current_user
from fastapi import Depends
from app.core.logger import log_info, log_error

async def handle_send_message(sio: AsyncServer, sid: str, data: dict, db=Depends(get_db)):
    """Handle incoming chat messages and send AI response."""
    try:
        user_id = (await get_current_user(data.get("token", "")))["uid"]
        message = ChatMessageCreate(
            user_id=user_id,
            role="user",
            content=data["content"],
            timestamp=data.get("timestamp")
        )
        ai_response = send_message(db, message, user_id, ai_model="gemini")
        await sio.emit("receive_message", {
            "id": ai_response.id,
            "content": ai_response.content,
            "role": ai_response.role,
            "timestamp": ai_response.timestamp.isoformat()
        }, room=sid)
        log_info(f"Message sent to user {user_id}: {ai_response.content}")
    except Exception as e:
        log_error(f"Error handling message: {str(e)}")
        await sio.emit("error", {"detail": "Failed to process message"}, room=sid)