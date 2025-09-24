from app.schemas import  UserCreate, UserResponse,UserLogin
from fastapi import FastAPI, HTTPException, Response, status, Depends, APIRouter
from app.models import  User
from app.utils import hash, compare
from sqlmodel import select
from app.database import  get_db, Session
from typing import List

router =APIRouter(
    prefix='/users',
    tags=['Users']
)

@router.post('',status_code=status.HTTP_201_CREATED,response_model=UserResponse)
def create_user(user:UserCreate,db:Session = Depends(get_db)):
    hashed_password = hash(user.password)
    user.password = hashed_password

    user_data = User(**user.model_dump())
    db.add(user_data)
    db.commit()
    db.refresh(user_data)
    return user_data


@router.get('',status_code=status.HTTP_200_OK,response_model=List[UserResponse])
def get_users(db:Session = Depends(get_db)):
    users = db.exec(select(User)).all()
    return users


@router.get('/{id}',status_code=status.HTTP_200_OK,response_model=UserResponse)
def get_users(id:int,db:Session = Depends(get_db)):
    user = db.get(User,id)
#    print(user)
    if not user:
            raise HTTPException(status_code=404, detail=f"User with {id} not found")
    return user