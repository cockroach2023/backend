from typing import Optional
from pydantic import BaseModel


class UserBase(BaseModel):
    pass


class UserLogin(BaseModel):
    username: str
    password: str


class UserCreate(UserLogin):
    activity_area: str
    nickname: str
    profile: str = None


class User(UserCreate):
    user_id: int
    is_admin: Optional[bool] = False
    is_blocked: Optional[bool] = False

    class Config:
        from_attribute = True
