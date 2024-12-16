from pydantic import BaseModel

class UserBase(BaseModel):
    username: str
    role: str
    email: str
    mobile_number: str
    age: int
    class Config:
        orm_mode = True

class UserCreate(UserBase):
    password: str

class UserUpdate(UserBase):
    pass

class User(UserBase):
    user_id: int

    class Config:
        orm_mode = True
