from datetime import date
from pydantic import BaseModel


# This is the Pydantic model schema
class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True


class PostCreate(PostBase):
    pass
