from pydantic import BaseModel


class UserBase(BaseModel):
    username: str


class UserPassword(BaseModel):
    password: str


class UserCreate(UserBase):
    password: str
    activity_area: str
    nickname: str
    profile: str


class User(UserBase):
    user_id: int
    activity_area: str
    nickname: str
    profile: str
    is_admin: bool
    is_blocked: bool

    class Config:
        from_attribute = True
