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

from . import models
from .database import engine
from .routers import post, user, auth

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


app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)


@app.get("/")
async def root():
    return {"message": "This is my API"}
