from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time

app = FastAPI()


class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None

try:
    conn = psycopg2.connect(host='localhost', database='fastapi',
                            user='postgres', password='postgres')
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


@app.get("/posts")
def get_posts():
    cursor.execute("SELECT * FROM posts")
    posts = cursor.fetchall()
    return {"data": posts}


@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(post: Post):
    cursor.execute(
        """INSERT INTO posts (title, content, published) VALUES (%s, %s, %s)
        RETURNING *""",
        (post.title, post.content, post.published),
    )
    new_post = cursor.fetchone()
    conn.commit()
    return {"data": f"Created post: {new_post}"}


@app.get("/posts/latest")
def get_latest_post():
    return {"data": my_posts[-1]}


@app.get("/posts/{id}")
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
def update_post(id: int, post: Post):
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
