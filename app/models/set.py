from sqlalchemy import Column, String, Integer, Float, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base import Base

class Set(Base):
    __tablename__ = "sets"

    id = Column(String, primary_key=True)
    exercise_id = Column(String, ForeignKey("exercises.id"))
    set_number = Column(Integer)
    reps = Column(Integer)
    weight = Column(Float)  # kg
    completed = Column(Boolean, default=False)

    exercise = relationship("Exercise", back_populates="sets")