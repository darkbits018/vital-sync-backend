from sqlalchemy import Column, String, Integer, Float, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base import Base

class Exercise(Base):
    __tablename__ = "exercises"

    id = Column(String, primary_key=True)
    workout_id = Column(String, ForeignKey("workouts.id"))
    name = Column(String)
    rest_time = Column(Integer)  # seconds
    notes = Column(String, nullable=True)

    workout = relationship("Workout", back_populates="exercises")
    sets = relationship("Set", back_populates="exercise")