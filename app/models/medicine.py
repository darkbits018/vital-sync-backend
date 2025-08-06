from sqlalchemy import Column, String, String, Integer, Boolean
from app.db.base import Base

class Medicine(Base):
    __tablename__ = "medicines"

    id = Column(String, primary_key=True)
    name = Column(String)
    dosage = Column(String)
    frequency = Column(Integer)  # times per day
    reminder_enabled = Column(Boolean, default=True)