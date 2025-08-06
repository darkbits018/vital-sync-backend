from pydantic import BaseModel
from typing import Optional

from app.schemas import UserInDB


class FirebaseUser(BaseModel):
    uid: str
    email: Optional[str]
    name: Optional[str]
    email_verified: bool

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    user_id: str

class SignupRequest(BaseModel):
        id_token: str
        username: str
        email: str | None = None
        name: str | None = None
        height: float
        weight: float
        age: int
        gender: str
        goal: str
        activity_level: str

class UserResponse(BaseModel):
        user: UserInDB