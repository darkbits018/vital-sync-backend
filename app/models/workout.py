from sqlalchemy import Column, String, DateTime, ForeignKey, Boolean, Integer
from sqlalchemy.orm import relationship
from app.db.base import Base
from datetime import datetime

from app.models.user import User


class Workout(Base):
    __tablename__ = "workouts"

    id = Column(String, primary_key=True)
    user_id = Column(String, ForeignKey("users.id"))
    name = Column(String)
    start_time = Column(DateTime)
    end_time = Column(DateTime, nullable=True)
    duration = Column(Integer, nullable=True)  # seconds
    notes = Column(String, nullable=True)
    is_template = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="workouts")
    exercises = relationship("Exercise", back_populates="workout")
    images = relationship("WorkoutImage", back_populates="workout")

User.workouts = relationship("Workout", order_by=Workout.start_time.desc(), back_populates="user")
