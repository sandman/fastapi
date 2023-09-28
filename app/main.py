from fastapi import FastAPI
from . import models
from .database import engine
from .routers import post, user, auth

# Init the FastAPI app
app = FastAPI()

# Import the models created in Alchemy from models.py
models.Base.metadata.create_all(bind=engine)


app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)


@app.get("/")
async def root():
    return {"message": "This is my API"}
