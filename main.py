from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
from random import randrange

app = FastAPI()


class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None


my_posts = [
    {"title": "Title of post 1", "content": "Content of post 1", "id": 1},
    {
        "title": "Favorite pizza recipe",
        "content": "Neapolitan pizza 101",
        "id": 2,
    },
]


def find_index_post(id):
    for i, post in enumerate(my_posts):
        if post["id"] == id:
            return i
    return None


@app.get("/")
async def root():
    return {"message": "This is my API"}


@app.get("/posts")
def get_posts():
    return {"data": my_posts}


@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(post: Post):
    post_dict = post.model_dump()
    post_dict["id"] = randrange(100000)
    my_posts.append(post_dict)
    return {"data": post_dict}


@app.get("/posts/latest")
def get_latest_post():
    return {"data": my_posts[-1]}


@app.get("/posts/{id}")
def get_post(id: int):
    post = next((post for post in my_posts if post["id"] == id), None)
    if post is None:
        raise HTTPException(
            detail=f"Post with id {id} not found",
            status_code=status.HTTP_404_NOT_FOUND,
        )

    return {"post detail": post}


@app.delete("/posts/{id}", status_code=status.HTTP_201_CREATED)
def delete_post(id: int):
    post = next((post for post in my_posts if post["id"] == id), None)
    if post is None:
        raise HTTPException(
            detail=f"Post with id {id} not found",
            status_code=status.HTTP_404_NOT_FOUND,
        )
    my_posts.remove(post)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    index = find_index_post(id)
    if index is None:
        raise HTTPException(
            detail=f"Post with id {id} not found",
            status_code=status.HTTP_404_NOT_FOUND,
        )
    post_dict = post.model_dump()
    post_dict["id"] = id
    my_posts[index] = post_dict

    return {"Updated post": post_dict}
