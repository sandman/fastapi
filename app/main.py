from fastapi import FastAPI, Response, status, HTTPException, Depends
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional, List
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import RedirectResponse

from sqlalchemy.orm import Session
from sqlalchemy.sql.functions import mode

from . import models, schemas
from .database import engine, get_db

# Init the FastAPI app
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)

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


@app.get("/sqlalchemy")
def test_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return {"status": posts}


@app.get("/posts", response_model=List[schemas.Post])
def get_posts(db: Session = Depends(get_db)):
    ## ORM implementation (without SQL)
    posts = db.query(models.Post).all()

    ## SQL Implementation (no ORM)
    # cursor.execute("SELECT * FROM posts")
    # posts = cursor.fetchall()
    return {"data": posts}


@app.post("/posts", response_model=List[schemas.Post])
def create_posts(post: models.Post, db: Session = Depends(get_db)):
    ## ORM implementation (without SQL)
    new_post = models.Post(**post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    ## SQL implementation (without ORM)
    # cursor.execute(
    #     """INSERT INTO posts (title, content, published) VALUES (%s, %s, %s)
    #     RETURNING *""",
    #     (post.title, post.content, post.published),
    # )
    # new_post = cursor.fetchone()
    # conn.commit()
    return {"data": new_post}


@app.get("/posts/{id}", response_model=None)
def get_post(id: int):
    cursor.execute("SELECT * FROM posts WHERE id = %s", (id,))
    post = cursor.fetchone()
    if post is None:
        raise HTTPException(
            detail=f"Post with id {id} not found",
            status_code=status.HTTP_404_NOT_FOUND,
        )

    return {"data:": f"Found post: {post}"}


@app.delete("/posts/{id}", status_code=status.HTTP_201_CREATED)
def delete_post(id: int):
    cursor.execute("DELETE FROM posts WHERE id = %s RETURNING *", (id,))
    post = cursor.fetchone()
    conn.commit()
    if post is None:
        raise HTTPException(
            detail=f"Post with id {id} not found",
            status_code=status.HTTP_404_NOT_FOUND,
        )
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{id}")
def update_post(id: int, post: models.Post):
    cursor.execute(
        """UPDATE posts SET title = %s, content = %s, published = %s
        WHERE id = %s RETURNING *""",
        (post.title, post.content, post.published, id),
    )
    updated_post = cursor.fetchone()
    conn.commit()
    if updated_post is None:
        raise HTTPException(
            detail=f"Post with id {id} not found",
            status_code=status.HTTP_404_NOT_FOUND,
        )

    return {"data": f"Updated post: {updated_post}"}
