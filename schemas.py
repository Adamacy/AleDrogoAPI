from pydantic import BaseModel

#Offer models
class ItemBase(BaseModel):
    title: str
    description: str | None = None
    price: float

class ItemCreate(ItemBase):
    pass

class Item(ItemBase):
    id: int
    owner_id: int
    
    class Config:
        orm_mode = True


#User models
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
    items: list[Item] = []

    class Config:
        orm_mode = True

class SessionData(BaseModel):
    username: str

    