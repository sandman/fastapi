from fastapi import FastAPI, Response, status, HTTPException, Depends
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional, List
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from fastapi.middleware.cors import CORSMiddleware

from sqlalchemy.orm import Session

from . import models, schemas
from .database import engine, get_db

# Init the FastAPI app
app = FastAPI()

# Import the models created in Alchemy from models.py
models.Base.metadata.create_all(bind=engine)


while True:
    try:
        conn = psycopg2.connect(
            database="fastapi",
            user="postgres",
            password="postgres",
            host="localhost",
            port="5432",
            cursor_factory=RealDictCursor,
        )
        cursor = conn.cursor()
        print("Database connection established")
        break
    except Exception as error:
        print(f"Connecting to database failed: {error}")
        time.sleep(2)


@app.get("/")
async def root():
    return {"message": "This is my API"}


@app.get("/posts", response_model=List[schemas.Post])
def get_posts(db: Session = Depends(get_db)):
    # # ORM implementation (without SQL)
    posts = db.query(models.Post).all()

    # # SQL Implementation (no ORM)
    # cursor.execute("SELECT * FROM posts")
    # posts = cursor.fetchall()
    return posts


@app.post(
    "/posts", status_code=status.HTTP_201_CREATED, response_model=schemas.Post
)
def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db)):
    # # ORM implementation (without SQL)
    new_post = models.Post(**post.model_dump())

    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    # # SQL implementation (without ORM)
    # cursor.execute(
    #     """INSERT INTO posts (title, content, published) VALUES (%s, %s, %s)
    #     RETURNING *""",
    #     (post.title, post.content, post.published),
    # )
    # new_post = cursor.fetchone()
    # conn.commit()
    return new_post


@app.get(
    "/posts/{id}", status_code=status.HTTP_200_OK, response_model=schemas.Post
)
def get_post(id: int, db: Session = Depends(get_db)):
    # # ORM implementation (without SQL)
    post = db.query(models.Post).filter(models.Post.id == id).first()
    # # SQL implementation (without ORM)
    # cursor.execute("SELECT * FROM posts WHERE id = %s", (id,))
    # post = cursor.fetchone()
    if post is None:
        raise HTTPException(
            detail=f"Post with id {id} not found",
            status_code=status.HTTP_404_NOT_FOUND,
        )

    return post


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db)):
    # # ORM implementation (without SQL)
    post = db.query(models.Post).filter(models.Post.id == id)
    # # SQL implementation (without ORM)
    # cursor.execute("DELETE FROM posts WHERE id = %s RETURNING *", (id,))
    # post = cursor.fetchone()
    # conn.commit()
    if post.first() is None:
        raise HTTPException(
            detail=f"Post with id {id} not found",
            status_code=status.HTTP_404_NOT_FOUND,
        )

    post.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{id}")
def update_post(
    id: int, post: schemas.PostCreate, db: Session = Depends(get_db)
):
    # ORM implementation (without SQL)
    post_query = db.query(models.Post).filter(models.Post.id == id)
    updated_post = post_query.first()
    # # SQL Implementation (without ORM)
    # cursor.execute(
    #     """UPDATE posts SET title = %s, content = %s, published = %s
    #     WHERE id = %s RETURNING *""",
    #     (post.title, post.content, post.published, id),
    # )
    # updated_post = cursor.fetchone()
    # conn.commit()
    if updated_post is None:
        raise HTTPException(
            detail=f"Post with id {id} not found",
            status_code=status.HTTP_404_NOT_FOUND,
        )

    post_query.update(post.model_dump(), synchronize_session=False)
    db.commit()
    return post
