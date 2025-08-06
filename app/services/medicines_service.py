from sqlalchemy.orm import Session
from app.models.medicine import Medicine as MedicineModel
from app.schemas.medicine import Medicine, MedicineCreate, MedicineUpdate


def get_medicines(db: Session, user_id: str, skip: int = 0, limit: int = 100) -> list[Medicine]:
    return db.query(MedicineModel).filter(MedicineModel.user_id == user_id).offset(skip).limit(limit).all()


def get_medicine(db: Session, medicine_id: str, user_id: str) -> Medicine:
    return db.query(MedicineModel).filter(
        MedicineModel.id == medicine_id,
        MedicineModel.user_id == user_id
    ).first()


def create_medicine(db: Session, medicine: MedicineCreate, user_id: str) -> Medicine:
    db_medicine = MedicineModel(**medicine.dict(), user_id=user_id)
    db.add(db_medicine)
    db.commit()
    db.refresh(db_medicine)
    return db_medicine


def update_medicine(db: Session, medicine_id: str, medicine_update: MedicineUpdate, user_id: str) -> Medicine:
    db_medicine = get_medicine(db, medicine_id, user_id)

    if not db_medicine:
        return None

    # Update fields
    update_data = medicine_update.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_medicine, key, value)

    db.commit()
    db.refresh(db_medicine)
    return db_medicine


def delete_medicine(db: Session, medicine_id: str, user_id: str) -> bool:
    db_medicine = get_medicine(db, medicine_id, user_id)

    if not db_medicine:
        return False

    db.delete(db_medicine)
    db.commit()
    return True
