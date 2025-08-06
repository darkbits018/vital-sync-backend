from sqlalchemy import Column, String, Integer, Float, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base import Base

class PresetExercise(Base):
    __tablename__ = "preset_exercises"

    id = Column(String, primary_key=True)
    preset_id = Column(String, ForeignKey("workout_presets.id"))
    name = Column(String)
    rest_time = Column(Integer)  # seconds
    notes = Column(String, nullable=True)

    preset = relationship("WorkoutPreset", back_populates="exercises")
    sets = relationship("PresetSet", back_populates="exercise")