from sqlalchemy.orm import Session
from app.models.macro_target import MacroTarget as MacroTargetModel
from app.schemas.macro_target import MacroTarget, MacroTargetCreate, MacroTargetUpdate


def get_macro_targets(db: Session, user_id: str, date: str = None, skip: int = 0, limit: int = 100) -> list[
    MacroTarget]:
    query = db.query(MacroTargetModel).filter(MacroTargetModel.user_id == user_id)

    if date:
        query = query.filter(MacroTargetModel.date == date)

    return query.offset(skip).limit(limit).all()


def get_macro_target(db: Session, target_id: str, user_id: str) -> MacroTarget:
    return db.query(MacroTargetModel).filter(
        MacroTargetModel.id == target_id,
        MacroTargetModel.user_id == user_id
    ).first()


def create_macro_target(db: Session, target: MacroTargetCreate, user_id: str) -> MacroTarget:
    db_target = MacroTargetModel(**target.dict(), user_id=user_id)
    db.add(db_target)
    db.commit()
    db.refresh(db_target)
    return db_target


def update_macro_target(db: Session, target_id: str, target_update: MacroTargetUpdate, user_id: str) -> MacroTarget:
    db_target = get_macro_target(db, target_id, user_id)

    if not db_target:
        return None

    # Update fields
    update_data = target_update.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_target, key, value)

    db.commit()
    db.refresh(db_target)
    return db_target


def delete_macro_target(db: Session, target_id: str, user_id: str) -> bool:
    db_target = get_macro_target(db, target_id, user_id)

    if not db_target:
        return False

    db.delete(db_target)
    db.commit()
    return True
