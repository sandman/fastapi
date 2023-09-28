from datetime import datetime
from pydantic import BaseModel, EmailStr
from typing import Optional


# This is the Pydantic model schema


class UserCreate(BaseModel):
    email: EmailStr
    password: str

    class Config:
        from_attributes = True


class User(BaseModel):
    email: EmailStr
    created_at: datetime

    class Config:
        from_attributes = True


class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        from_attributes = True


class UserLogin(BaseModel):
    email: EmailStr
    password: str

    class Config:
        from_attributes = True


class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True

    def model_dump(self):
        return self.__dict__


class PostCreate(PostBase):
    pass


class Post(PostBase):
    id: int
    created_at: datetime
    owner_id: int
    owner: UserOut

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[int]
