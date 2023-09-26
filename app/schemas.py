from datetime import datetime
from pydantic import BaseModel


# This is the Pydantic model schema
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

    class Config:
        orm_mode = True
