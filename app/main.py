from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from . import models
from .database import engine
from .routers import posts, users, auth, votes

models.Base.metadata.create_all(bind=engine)
app = FastAPI()

origins = ["https://www.google.com",
           "http://localhost:8000",
           "http://127.0.0.1:8000",
           ]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(posts.router)
app.include_router(users.router)
app.include_router(auth.router)
app.include_router(votes.router)


@app.get("/")
async def root():
    return {"message": "Hello World"}
