from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.schemas.medicine import Medicine, MedicineCreate, MedicineUpdate
from app.db.session import get_db
from app.models.medicine import Medicine as MedicineModel
from app.services.firebase_auth import get_current_user

router = APIRouter()


@router.get("/", response_model=list[Medicine])
async def read_medicines(
        skip: int = 0,
        limit: int = 100,
        db: Session = Depends(get_db),
        current_user: dict = Depends(get_current_user)
):
    medicines = db.query(MedicineModel).filter(MedicineModel.user_id == current_user["uid"]).offset(skip).limit(
        limit).all()
    return medicines


@router.get("/{medicine_id}", response_model=Medicine)
async def read_medicine(
        medicine_id: str,
        db: Session = Depends(get_db),
        current_user: dict = Depends(get_current_user)
):
    medicine = db.query(MedicineModel).filter(
        MedicineModel.id == medicine_id,
        MedicineModel.user_id == current_user["uid"]
    ).first()

    if not medicine:
        raise HTTPException(status_code=404, detail="Medicine not found")
    return medicine


@router.post("/", response_model=Medicine, status_code=status.HTTP_201_CREATED)
async def create_medicine(
        medicine: MedicineCreate,
        db: Session = Depends(get_db),
        current_user: dict = Depends(get_current_user)
):
    db_medicine = MedicineModel(**medicine.dict(), user_id=current_user["uid"])
    db.add(db_medicine)
    db.commit()
    db.refresh(db_medicine)
    return db_medicine


@router.put("/{medicine_id}", response_model=Medicine)
async def update_medicine(
        medicine_id: str,
        medicine_update: MedicineUpdate,
        db: Session = Depends(get_db),
        current_user: dict = Depends(get_current_user)
):
    db_medicine = db.query(MedicineModel).filter(
        MedicineModel.id == medicine_id,
        MedicineModel.user_id == current_user["uid"]
    ).first()

    if not db_medicine:
        raise HTTPException(status_code=404, detail="Medicine not found")

    # Update fields
    update_data = medicine_update.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_medicine, key, value)

    db.commit()
    db.refresh(db_medicine)
    return db_medicine


@router.delete("/{medicine_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_medicine(
        medicine_id: str,
        db: Session = Depends(get_db),
        current_user: dict = Depends(get_current_user)
):
    db_medicine = db.query(MedicineModel).filter(
        MedicineModel.id == medicine_id,
        MedicineModel.user_id == current_user["uid"]
    ).first()

    if not db_medicine:
        raise HTTPException(status_code=404, detail="Medicine not found")

    db.delete(db_medicine)
    db.commit()
    return {"message": "Medicine deleted successfully"}
