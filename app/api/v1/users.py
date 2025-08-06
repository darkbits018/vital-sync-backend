from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.schemas.user import UserInDB, UserUpdate
from app.db.session import get_db
from app.models.user import User
from app.services.firebase_auth import get_current_user

router = APIRouter()


@router.get("/me", response_model=UserInDB)
async def read_users_me(
        current_user: dict = Depends(get_current_user),
        db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.id == current_user["uid"]).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.put("/me", response_model=UserInDB)
async def update_user_me(
        user_update: UserUpdate,
        current_user: dict = Depends(get_current_user),
        db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.id == current_user["uid"]).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Update user fields
    if user_update.name is not None:
        user.name = user_update.name
    if user_update.avatar_url is not None:
        user.avatar_url = user_update.avatar_url

    db.commit()
    db.refresh(user)
    return user
