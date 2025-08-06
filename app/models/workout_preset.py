from datetime import datetime

from sqlalchemy import Column, String, Integer, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from app.db.base import Base

class WorkoutPreset(Base):
    __tablename__ = "workout_presets"

    id = Column(String, primary_key=True)
    name = Column(String)
    category = Column(String)
    estimated_duration = Column(Integer)  # minutes
    estimated_calories = Column(Integer)
    created_at = Column(DateTime, default=datetime.utcnow)

    exercises = relationship("PresetExercise", back_populates="preset")