from fastapi import FastAPI
from app.database import create_db_and_tables
from app.routes import redditposts, users, auth,votes
from app.config import Settings
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import SQLModel



create_db_and_tables()
app = FastAPI()

origin =['*']
app.add_middleware(
    CORSMiddleware,
    allow_origins=origin,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(redditposts.router)
app.include_router(users.router)
app.include_router(auth.router)
app.include_router(votes.router)

