from sqlmodel import SQLModel, Field, TIMESTAMP, Column, text, Relationship
from datetime import datetime
from typing import Optional, List

class RedditPost(SQLModel, table=True):
    __tablename__ = 'redditposts'
    id: int | None = Field(default=None, primary_key=True)
    content: str = Field(index=True, nullable=False)
    title: str | None = Field(default=None, index=True, nullable=False)
    publish: bool | None = Field(default=True,index=True,nullable=False)
    register_at: Optional[datetime] = Field(sa_column=Column(TIMESTAMP(timezone=True), nullable=False,server_default=text("CURRENT_TIMESTAMP")))
    user_id : int  = Field(foreign_key="users.id",ondelete='CASCADE',nullable=False)
    user: "User" = Relationship(back_populates="redditposts")

class User(SQLModel,table=True):
    __tablename__ ='users'
    id: int | None = Field(default=None, primary_key=True)
    email: str| None = Field(nullable=False, unique=True)
    password: str|None =Field(nullable=False)
    register_at: Optional[datetime] = Field(sa_column=Column(TIMESTAMP(timezone=True), nullable=False,server_default=text("CURRENT_TIMESTAMP")))
    redditposts: List[RedditPost] = Relationship(back_populates="user")

class Votes(SQLModel,table=True):
    __tablename__ ='votes'
    redditposts_id: int |None = Field(foreign_key='redditposts.id',ondelete='CASCADE',primary_key=True)
    user_id: int |None = Field(foreign_key='users.id',ondelete='CASCADE',primary_key=True)