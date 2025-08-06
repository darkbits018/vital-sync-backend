from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.schemas.preference import Preference, PreferenceCreate, PreferenceUpdate
from app.db.session import get_db
from app.models.preference import Preference as PreferenceModel
from app.services.firebase_auth import get_current_user

router = APIRouter()


@router.get("/me", response_model=Preference)
async def read_preferences(
        db: Session = Depends(get_db),
        current_user: dict = Depends(get_current_user)
):
    preference = db.query(PreferenceModel).filter(PreferenceModel.user_id == current_user["uid"]).first()

    if not preference:
        raise HTTPException(status_code=404, detail="Preferences not found")
    return preference


@router.post("/", response_model=Preference, status_code=status.HTTP_201_CREATED)
async def create_preferences(
        preference: PreferenceCreate,
        db: Session = Depends(get_db),
        current_user: dict = Depends(get_current_user)
):
    db_preference = PreferenceModel(**preference.dict(), user_id=current_user["uid"])
    db.add(db_preference)
    db.commit()
    db.refresh(db_preference)
    return db_preference


@router.put("/", response_model=Preference)
async def update_preferences(
        preference_update: PreferenceUpdate,
        db: Session = Depends(get_db),
        current_user: dict = Depends(get_current_user)
):
    db_preference = db.query(PreferenceModel).filter(PreferenceModel.user_id == current_user["uid"]).first()

    if not db_preference:
        raise HTTPException(status_code=404, detail="Preferences not found")

    # Update fields
    update_data = preference_update.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_preference, key, value)

    db.commit()
    db.refresh(db_preference)
    return db_preference
