from sqlalchemy import Column, String, Integer, Float, Boolean
from sqlalchemy.orm import relationship

from app.db.base import Base


class Food(Base):
    __tablename__ = "foods"

    id = Column(String, primary_key=True)
    name = Column(String)
    calories = Column(Integer)
    protein = Column(Float)
    carbs = Column(Float)
    fat = Column(Float)
    fiber = Column(Float)
    sugar = Column(Float)
    sodium = Column(Integer)
    category = Column(String)
    is_custom = Column(Boolean, default=True)

    meals = relationship("Meal", secondary="meal_foods", back_populates="foods")  # Reference string "meal_foods"
