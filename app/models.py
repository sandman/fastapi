from .database import Base
from sqlalchemy import Column, Integer, String, Boolean, TIMESTAMP, text


# This is the sqlalchemy model schema
class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, nullable=False, index=True)
    title = Column(String(50), nullable=False)
    content = Column(String(500), nullable=False)
    published = Column(Boolean, server_default="TRUE", nullable=False)
    created_at = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=text("now()")
    )

    # def __repr__(self):
    #     return f"<Post {self.title}>"


class User(Base):
    __tablename__ = "users"

    email = Column(String(50), nullable=False, unique=True)
    password = Column(String, nullable=False)
    id = Column(Integer, primary_key=True, nullable=False, index=True)
    created_at = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=text("now()")
    )
