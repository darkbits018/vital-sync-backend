from pydantic import BaseModel
from datetime import date
from typing import Optional


class MacroTargetBase(BaseModel):
    calories: float
    protein: float
    carbs: float
    fat: float
    date: date


class MacroTargetCreate(MacroTargetBase):
    user_id: str


class MacroTargetUpdate(BaseModel):
    calories: Optional[float] = None
    protein: Optional[float] = None
    carbs: Optional[float] = None
    fat: Optional[float] = None
    date: Optional[date] = None


class MacroTarget(MacroTargetBase):
    id: str
    user_id: str

    class Config:
        from_attributes = True
