from pydantic import BaseModel
from typing import Optional


class WorkoutImageBase(BaseModel):
    url: str
    description: Optional[str] = None


class WorkoutImageCreate(WorkoutImageBase):
    pass


class WorkoutImage(WorkoutImageBase):
    id: str
    workout_id: str

    class Config:
        from_attributes = True
