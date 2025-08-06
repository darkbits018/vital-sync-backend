from pydantic import BaseModel
from typing import Optional


class FoodBase(BaseModel):
    name: str
    calories: float
    protein: float
    carbs: float
    fat: float


class FoodCreate(FoodBase):
    pass


class Food(FoodBase):
    id: str

    class Config:
        from_attributes = True
