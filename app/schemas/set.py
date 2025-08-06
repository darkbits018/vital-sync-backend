from pydantic import BaseModel
from typing import Optional


class SetBase(BaseModel):
    set_number: int
    reps: int
    weight: float
    completed: bool


class SetCreate(SetBase):
    pass


class SetUpdate(BaseModel):
    set_number: Optional[int] = None
    reps: Optional[int] = None
    weight: Optional[float] = None
    completed: Optional[bool] = None


class Set(SetBase):
    id: str

    class Config:
        from_attributes = True
