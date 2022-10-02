from pydantic import BaseModel


class UserBase(BaseModel):
    nickname: str
    fullname: str
    email: str

class UserLogin(BaseModel):
    email: str
    password: str

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    is_active: bool

    class Config:
        orm_mode = True

class SessionData(BaseModel):
    username: str

    