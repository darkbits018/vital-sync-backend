from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.schemas.macro_target import MacroTarget, MacroTargetCreate, MacroTargetUpdate
from app.db.session import get_db
from app.models.macro_target import MacroTarget as MacroTargetModel
from app.services.firebase_auth import get_current_user

router = APIRouter()


@router.get("/targets", response_model=list[MacroTarget])
async def read_macro_targets(
        date: str = None,
        skip: int = 0,
        limit: int = 100,
        db: Session = Depends(get_db),
        current_user: dict = Depends(get_current_user)
):
    query = db.query(MacroTargetModel).filter(MacroTargetModel.user_id == current_user["uid"])

    if date:
        query = query.filter(MacroTargetModel.date == date)

    targets = query.offset(skip).limit(limit).all()
    return targets


@router.get("/targets/{target_id}", response_model=MacroTarget)
async def read_macro_target(
        target_id: str,
        db: Session = Depends(get_db),
        current_user: dict = Depends(get_current_user)
):
    target = db.query(MacroTargetModel).filter(
        MacroTargetModel.id == target_id,
        MacroTargetModel.user_id == current_user["uid"]
    ).first()

    if not target:
        raise HTTPException(status_code=404, detail="Macro target not found")
    return target


@router.post("/targets", response_model=MacroTarget, status_code=status.HTTP_201_CREATED)
async def create_macro_target(
        target: MacroTargetCreate,
        db: Session = Depends(get_db),
        current_user: dict = Depends(get_current_user)
):
    db_target = MacroTargetModel(**target.dict(), user_id=current_user["uid"])
    db.add(db_target)
    db.commit()
    db.refresh(db_target)
    return db_target


@router.put("/targets/{target_id}", response_model=MacroTarget)
async def update_macro_target(
        target_id: str,
        target_update: MacroTargetUpdate,
        db: Session = Depends(get_db),
        current_user: dict = Depends(get_current_user)
):
    db_target = db.query(MacroTargetModel).filter(
        MacroTargetModel.id == target_id,
        MacroTargetModel.user_id == current_user["uid"]
    ).first()

    if not db_target:
        raise HTTPException(status_code=404, detail="Macro target not found")

    # Update fields
    update_data = target_update.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_target, key, value)

    db.commit()
    db.refresh(db_target)
    return db_target


@router.delete("/targets/{target_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_macro_target(
        target_id: str,
        db: Session = Depends(get_db),
        current_user: dict = Depends(get_current_user)
):
    db_target = db.query(MacroTargetModel).filter(
        MacroTargetModel.id == target_id,
        MacroTargetModel.user_id == current_user["uid"]
    ).first()

    if not db_target:
        raise HTTPException(status_code=404, detail="Macro target not found")

    db.delete(db_target)
    db.commit()
    return {"message": "Macro target deleted successfully"}
