from sqlalchemy import Column, String, JSON
from app.db.base import Base

class Preference(Base):
    __tablename__ = "preferences"

    id = Column(String, primary_key=True)
    user_id = Column(String, unique=True)
    general = Column(JSON)
    eating_habits = Column(JSON)
    health_goals = Column(JSON)
    notifications = Column(JSON)