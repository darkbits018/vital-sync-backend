from pydantic import BaseModel
from typing import Optional


class PresetSetBase(BaseModel):
    set_number: int
    reps: int
    weight: float


class PresetSetCreate(PresetSetBase):
    pass


class PresetSet(PresetSetBase):
    id: str
    preset_exercise_id: str

    class Config:
        from_attributes = True
