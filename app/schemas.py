from datetime import date
from pydantic import BaseModel


class Post(BaseModel):
    id: int
    title: str
    content: str
    published: bool
    created_at: date

    class Config:
        orm_mode = True
