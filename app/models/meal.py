from sqlalchemy import Column, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base import Base
from datetime import datetime


class Meal(Base):
    __tablename__ = "meals"

    id = Column(String, primary_key=True)
    user_id = Column(String, ForeignKey("users.id"))
    name = Column(String)
    meal_type = Column(String)  # breakfast, lunch, dinner, snack
    date = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="meals")
    foods = relationship("Food", secondary="meal_foods", back_populates="meals")  # Reference string "meal_foods"
