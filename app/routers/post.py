from fastapi import (
    FastAPI,
    Response,
    status,
    HTTPException,
    Depends,
    APIRouter,
)
from .. import models, schemas, oauth2
from ..database import get_db
from sqlalchemy.orm import Session
from typing import List

router = APIRouter(prefix="/posts", tags=["posts"])


@router.get("/", response_model=List[schemas.Post])
def get_posts(
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user),
):
    # # ORM implementation (without SQL)
    posts = db.query(models.Post).all()

    return posts


@router.post(
    "/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post
)
def create_posts(
    post: schemas.PostCreate,
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user),
):
    # # ORM implementation (without SQL)
    new_post = models.Post(owner_id=current_user.id, **post.model_dump())

    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post


@router.get(
    "/{id}", status_code=status.HTTP_200_OK, response_model=schemas.Post
)
def get_post(
    id: int,
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user),
):
    # # ORM implementation (without SQL)
    post = db.query(models.Post).filter(models.Post.id == id).first()

    if post is None:
        raise HTTPException(
            detail=f"Post with id {id} not found",
            status_code=status.HTTP_404_NOT_FOUND,
        )

    return post


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(
    id: int,
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user),
):
    # # ORM implementation (without SQL)
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    if post is None:
        raise HTTPException(
            detail=f"Post with id {id} not found",
            status_code=status.HTTP_404_NOT_FOUND,
        )

    if post.owner_id != current_user.id:
        raise HTTPException(
            detail=f"User with id {current_user.id} is not the owner of the post with id {id}",
            status_code=status.HTTP_403_FORBIDDEN,
        )

    post_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put(
    "/{id}", status_code=status.HTTP_200_OK, response_model=schemas.Post
)
def update_post(
    id: int,
    updated_post: schemas.PostCreate,
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user),
):
    # ORM implementation (without SQL)
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()

    if post is None:
        raise HTTPException(
            detail=f"Post with id {id} not found ",
            status_code=status.HTTP_404_NOT_FOUND,
        )

    if post.owner_id != current_user.id:
        raise HTTPException(
            detail=f"User with id {current_user.id} is not the owner of the post with id {id}",
            status_code=status.HTTP_403_FORBIDDEN,
        )

    post_query.update(updated_post.model_dump(), synchronize_session=False)
    db.commit()
    return post_query.first()
