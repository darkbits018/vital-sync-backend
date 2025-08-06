from datetime import datetime
from sqlalchemy import Column, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from app.db.base import Base

class WorkoutImage(Base):
    __tablename__ = "workout_images"
    id = Column(String, primary_key=True)
    workout_id = Column(String, ForeignKey("workouts.id"))
    url = Column(String)
    uploaded_at = Column(DateTime, default=datetime.utcnow)
    workout = relationship("Workout", back_populates="images")