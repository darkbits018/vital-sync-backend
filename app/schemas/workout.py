from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List, Dict


class SetBase(BaseModel):
    set_number: int
    reps: int
    weight: float
    completed: bool


class SetCreate(SetBase):
    pass


class Set(SetBase):
    id: str

    class Config:
        from_attributes = True


class ExerciseBase(BaseModel):
    name: str
    rest_time: int
    notes: Optional[str] = None


class ExerciseCreate(ExerciseBase):
    sets: List[SetCreate]


class Exercise(ExerciseBase):
    id: str
    sets: List[Set]

    class Config:
        from_attributes = True


class WorkoutBase(BaseModel):
    name: str
    start_time: datetime
    end_time: Optional[datetime] = None
    duration: Optional[int] = None
    notes: Optional[str] = None
    is_template: bool = False


class WorkoutCreate(WorkoutBase):
    exercises: List[ExerciseCreate]


class WorkoutUpdate(WorkoutBase):
    name: Optional[str] = None
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    duration: Optional[int] = None
    notes: Optional[str] = None
    is_template: Optional[bool] = None


class Workout(WorkoutBase):
    id: str
    user_id: str
    created_at: datetime
    exercises: List[Exercise]

    class Config:
        from_attributes = True