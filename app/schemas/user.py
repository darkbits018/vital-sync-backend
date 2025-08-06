from pydantic import BaseModel, ConfigDict
from datetime import datetime


class UserBase(BaseModel):
    username: str
    email: str | None = None
    name: str | None = None


class UserCreate(UserBase):
    height: float
    weight: float
    age: int
    gender: str
    goal: str
    activity_level: str


class UserUpdate(UserBase):
    height: float | None = None
    weight: float | None = None
    age: int | None = None
    gender: str | None = None
    goal: str | None = None
    activity_level: str | None = None


class UserInDB(UserBase):
    model_config = ConfigDict(from_attributes=True)
    id: str
    email_verified: bool
    height: float
    weight: float
    age: int
    gender: str
    goal: str
    activity_level: str
    created_at: datetime
