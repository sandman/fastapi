from sqlalchemy.orm import Session
from fastapi import (
    FastAPI,
    Response,
    status,
    HTTPException,
    Depends,
    APIRouter,
)
from .. import models, schemas, utils
from ..database import get_db


router = APIRouter(prefix="/users", tags=["users"])


@router.post(
    "/", status_code=status.HTTP_201_CREATED, response_model=schemas.User
)
def create_user(user: schemas.UserCreate, db=Depends(get_db)):
    # Hash the password
    hashed_password = utils.hash(user.password)
    user.password = hashed_password
    new_user = models.User(**user.dict())

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


@router.get(
    "/{id}", status_code=status.HTTP_200_OK, response_model=schemas.User
)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if user is None:
        raise HTTPException(
            detail=f"User with id {id} not found",
            status_code=status.HTTP_404_NOT_FOUND,
        )

    return user
