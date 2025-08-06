from datetime import datetime

from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate, UserInDB


def get_user(db: Session, user_id: str) -> UserInDB:
    return db.query(User).filter(User.id == user_id).first()


def get_user_by_email(db: Session, email: str) -> UserInDB:
    return db.query(User).filter(User.email == email).first()


def create_user(db: Session, user: UserCreate) -> UserInDB:
    db_user = User(**user.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def update_user(db: Session, user_id: str, user_update: UserUpdate) -> UserInDB:
    db_user = get_user(db, user_id)

    if not db_user:
        return None

    # Update fields
    if user_update.name is not None:
        db_user.name = user_update.name
    if user_update.avatar_url is not None:
        db_user.avatar_url = user_update.avatar_url

    db.commit()
    db.refresh(db_user)
    return db_user


def sync_firebase_user(db: Session, firebase_data: dict) -> UserInDB:
    db_user = get_user(db, firebase_data["uid"])

    if not db_user:
        # Create new user from Firebase data
        db_user = User(
            id=firebase_data["uid"],
            email=firebase_data.get("email"),
            name=firebase_data.get("name"),
            email_verified=firebase_data.get("email_verified", False),
            created_at=datetime.utcnow()
        )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
    else:
        # Update existing user info
        if "email" in firebase_data:
            db_user.email = firebase_data["email"]
        if "name" in firebase_data:
            db_user.name = firebase_data["name"]

        db.commit()
        db.refresh(db_user)

    return db_user
