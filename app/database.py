
from fastapi import Depends, FastAPI
from sqlmodel import Field, Session, SQLModel, create_engine
from app.config import settings

DB_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}/{settings.database_name}'

engine = create_engine(DB_URL)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def get_db():
    with Session(engine) as session:
        yield session
