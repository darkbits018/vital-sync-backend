from pydantic import BaseModel
from typing import List, Optional


class ExerciseBase(BaseModel):
    name: str
    rest_time: int
    notes: Optional[str] = None


class ExerciseCreate(ExerciseBase):
    sets: List["SetCreate"]


class ExerciseUpdate(ExerciseBase):
    name: Optional[str] = None
    rest_time: Optional[int] = None
    notes: Optional[str] = None
    sets: Optional[List["SetCreate"]] = None


class Exercise(ExerciseBase):
    id: str
    sets: List["Set"]

    class Config:
        from_attributes = True
