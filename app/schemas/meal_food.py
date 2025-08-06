from pydantic import BaseModel
from typing import Optional
from .food import Food


class MealFoodBase(BaseModel):
    food_id: str
    quantity: float


class MealFoodCreate(MealFoodBase):
    name: str
    calories: float
    protein: float
    carbs: float
    fat: float


class MealFood(MealFoodBase):
    id: str
    food: Food

    class Config:
        from_attributes = True
