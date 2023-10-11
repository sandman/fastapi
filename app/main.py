from fastapi import FastAPI
from . import models
from .database import engine
from .routers import post, user, auth, vote
from .config import settings

# Init the FastAPI app
app = FastAPI()

# Import the models created in Alchemy from models.py
# This is commented out since we're using Alembic to manage our migrations
# models.Base.metadata.create_all(bind=engine)


app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)


@app.get("/")
async def root():
    return {"message": "This is my API"}
