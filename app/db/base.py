from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Table, Column, String, ForeignKey, Float

Base = declarative_base()

# Define meal_foods association table
meal_foods = Table(
    "meal_foods",
    Base.metadata,
    Column("meal_id", String, ForeignKey("meals.id")),
    Column("food_id", String, ForeignKey("foods.id")),
    Column("quantity", Float)
)

# Import models after defining meal_foods
from app.models.meal import Meal
from app.models.food import Food
from app.models.user import User