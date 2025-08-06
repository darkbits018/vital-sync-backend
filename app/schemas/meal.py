from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional

class FoodInMeal(BaseModel):
    food_id: str
    quantity: float

class MealCreate(BaseModel):
    id: str
    name: str
    meal_type: str
    date: datetime
    created_at: datetime
    foods: List[FoodInMeal] = []

class MealUpdate(BaseModel):
    name: Optional[str] = None
    meal_type: Optional[str] = None
    date: Optional[datetime] = None
    foods: Optional[List[FoodInMeal]] = None

class Food(BaseModel):
    id: str
    name: str
    calories: int
    protein: float
    carbs: float
    fat: float
    fiber: float
    sugar: float
    sodium: int
    category: str
    is_custom: bool

class Meal(BaseModel):
    id: str
    user_id: str
    name: str
    meal_type: str
    date: datetime
    created_at: datetime
    foods: List[FoodInMeal] = []