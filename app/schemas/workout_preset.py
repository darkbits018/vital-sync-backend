from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List


class PresetSetBase(BaseModel):
    set_number: int
    reps: int
    weight: float


class PresetSetCreate(PresetSetBase):
    pass


class PresetSet(PresetSetBase):
    id: str

    class Config:
        from_attributes = True


class PresetExerciseBase(BaseModel):
    name: str
    rest_time: int
    notes: Optional[str] = None


class PresetExerciseCreate(PresetExerciseBase):
    sets: List[PresetSetCreate]


class PresetExercise(PresetExerciseBase):
    id: str
    sets: List[PresetSet]

    class Config:
        from_attributes = True


class WorkoutPresetBase(BaseModel):
    name: str
    category: str
    estimated_duration: int
    estimated_calories: int


class WorkoutPresetCreate(WorkoutPresetBase):
    exercises: List[PresetExerciseCreate]


class WorkoutPresetUpdate(BaseModel):
    name: Optional[str] = None
    category: Optional[str] = None
    estimated_duration: Optional[int] = None
    estimated_calories: Optional[int] = None
    exercises: Optional[List["PresetExerciseCreate"]] = None  # ← Add this


class WorkoutPreset(WorkoutPresetBase):
    id: str
    created_at: datetime
    exercises: List[PresetExercise]

    class Config:
        from_attributes = True
