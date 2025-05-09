from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional


class UserBase(BaseModel):
    email:EmailStr
    class Config:
        from_attributes = True

class UserCreate(UserBase):
    password:str

class UserResponse(UserBase):
    id: int 
    register_at: datetime

class UserLogin(BaseModel):
    email:EmailStr
    password:str

class RedditPostBase(BaseModel):
    content: str 
    title: str 
    publish: bool 
    class Config:
        from_attributes = True
        #upack k time same object use karne k liye

class RedditPostResponse(RedditPostBase):
    id: int 
    register_at: datetime
    user_id : int
    user : UserResponse

class RedditPostResponseVotes(BaseModel):
    RedditPost :RedditPostResponse
    votes :int
    class Config:
        from_attributes = True

class RedditPostCreate(RedditPostBase):
    pass

class RedditPostUpdate(RedditPostBase):
    content: Optional[str] = None
    title: Optional[str] = None
    publish: Optional[bool] =None


class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[int] = None

class Vote(BaseModel):
    redditposts_id :int
