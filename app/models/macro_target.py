from sqlalchemy import Column, String, Integer, Float
from app.db.base import Base

class MacroTarget(Base):
    __tablename__ = "macro_targets"

    id = Column(String, primary_key=True)
    user_id = Column(String)
    calories = Column(Integer)
    protein = Column(Float)
    carbs = Column(Float)
    fat = Column(Float)
    fiber = Column(Float)
    sugar = Column(Float)
    sodium = Column(Integer)
    date = Column(String)  # YYYY-MM-DD