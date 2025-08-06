from sqlalchemy.orm import Session
from app.models.preference import Preference as PreferenceModel
from app.schemas.preference import Preference, PreferenceCreate, PreferenceUpdate


def get_preferences(db: Session, user_id: str) -> Preference:
    return db.query(PreferenceModel).filter(PreferenceModel.user_id == user_id).first()


def create_preferences(db: Session, preferences: PreferenceCreate, user_id: str) -> Preference:
    db_preference = PreferenceModel(**preferences.dict(), user_id=user_id)
    db.add(db_preference)
    db.commit()
    db.refresh(db_preference)
    return db_preference


def update_preferences(db: Session, preferences: PreferenceUpdate, user_id: str) -> Preference:
    db_preference = get_preferences(db, user_id)

    if not db_preference:
        return None

    # Update fields
    update_data = preferences.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_preference, key, value)

    db.commit()
    db.refresh(db_preference)
    return db_preference