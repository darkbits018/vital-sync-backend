from pydantic import BaseModel
from typing import List, Optional


class PresetExerciseBase(BaseModel):
    name: str
    rest_time: int
    notes: Optional[str] = None


class PresetExerciseCreate(PresetExerciseBase):
    sets: List["PresetSetCreate"]


class PresetExercise(PresetExerciseBase):
    id: str
    preset_id: str
    sets: List["PresetSet"]

    class Config:
        from_attributes = True
