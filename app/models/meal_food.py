from sqlalchemy import Table, Column, String, ForeignKey, Float
from app.db.base import Base

meal_foods = Table(
    "meal_foods",
    Base.metadata,
    Column("meal_id", String, ForeignKey("meals.id")),
    Column("food_id", String, ForeignKey("foods.id")),
    Column("quantity", Float)  # Optional: Keep for additional attributes like quantity
)