from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.services.firebase_auth import get_current_user
from app.models.notification import Notification as NotificationModel
from app.schemas.notification import Notification, NotificationCreate
from firebase_admin import messaging
from typing import List
from datetime import datetime

router = APIRouter()


@router.post("/", response_model=Notification, status_code=status.HTTP_201_CREATED)
async def create_notification(
        notification: NotificationCreate,
        db: Session = Depends(get_db),
        current_user: dict = Depends(get_current_user)
):
    """Create and send a push notification.

    Args:
        notification (NotificationCreate): Notification data.

    Returns:
        Notification: Created notification.
    """
    db_notification = NotificationModel(
        user_id=current_user["uid"],
        title=notification.title,
        body=notification.body,
        created_at=notification.created_at or datetime.utcnow()
    )
    db.add(db_notification)
    db.commit()
    db.refresh(db_notification)

    # Send push notification via FCM
    message = messaging.Message(
        notification=messaging.Notification(
            title=notification.title,
            body=notification.body
        ),
        token=current_user.get("fcm_token")  # Assumes FCM token stored in Firebase user data
    )
    try:
        messaging.send(message)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to send notification: {str(e)}")

    return db_notification


@router.get("/", response_model=List[Notification])
async def get_notifications(
        skip: int = 0,
        limit: int = 100,
        db: Session = Depends(get_db),
        current_user: dict = Depends(get_current_user)
):
    """Retrieve user's notification history.

    Args:
        skip (int): Number of records to skip (default: 0).
        limit (int): Maximum number of records to return (default: 100).

    Returns:
        List[Notification]: List of notifications.
    """
    return db.query(NotificationModel).filter(
        NotificationModel.user_id == current_user["uid"]
    ).offset(skip).limit(limit).all()
