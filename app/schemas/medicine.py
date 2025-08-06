from pydantic import BaseModel
from typing import Optional


class MedicineBase(BaseModel):
    name: str
    dosage: str
    frequency: int  # times per day
    reminder_enabled: Optional[bool] = True


class MedicineCreate(MedicineBase):
    pass


class MedicineUpdate(MedicineBase):
    name: Optional[str] = None
    dosage: Optional[str] = None
    frequency: Optional[int] = None
    reminder_enabled: Optional[bool] = None


class Medicine(MedicineBase):
    id: str

    class Config:
        from_attributes = True