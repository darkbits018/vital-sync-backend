from sqlalchemy import Column, String, Integer, Float, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base import Base

class PresetSet(Base):
    __tablename__ = "preset_sets"

    id = Column(String, primary_key=True)
    exercise_id = Column(String, ForeignKey("preset_exercises.id"))
    set_number = Column(Integer)
    reps = Column(Integer)
    weight = Column(Float)  # kg

    exercise = relationship("PresetExercise", back_populates="sets")