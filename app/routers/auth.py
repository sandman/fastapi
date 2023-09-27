from fastapi import APIRouter, Depends, Response, HTTPException, status
from sqlalchemy.orm import Session
from ..database import get_db

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/login", status_code=status.HTTP_200_OK)
def login(db: Session = Depends(get_db)):
    pass
