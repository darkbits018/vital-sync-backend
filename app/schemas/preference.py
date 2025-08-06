from pydantic import BaseModel
from typing import Dict, Any, Optional


class PreferenceBase(BaseModel):
    user_id: str
    general: Dict[str, Any]
    eating_habits: Dict[str, Any]
    health_goals: Dict[str, Any]
    notifications: Dict[str, Any]


class PreferenceCreate(PreferenceBase):
    pass


class PreferenceUpdate(PreferenceBase):
    general: Optional[Dict[str, Any]] = None
    eating_habits: Optional[Dict[str, Any]] = None
    health_goals: Optional[Dict[str, Any]] = None
    notifications: Optional[Dict[str, Any]] = None


class Preference(PreferenceBase):
    id: str

    class Config:
        from_attributes = True