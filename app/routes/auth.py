from fastapi import  HTTPException,  status, Depends, APIRouter
from app.models import  User
from app.utils import  compare
from sqlmodel import select
from app.database import  get_db, Session
from app import oauth2, schemas
from fastapi.security import  OAuth2PasswordRequestForm

router =APIRouter(
    prefix='/login',
    tags=['Authentication']
)

@router.post('',status_code=status.HTTP_201_CREATED,response_model=schemas.Token)
def login(user:OAuth2PasswordRequestForm= Depends(),db:Session = Depends(get_db)):
    user_db = db.exec(select(User).where(User.email == user.username)).one_or_none()
    if user is None:
        raise HTTPException(status_code=403, detail=f"Invalid credentials")
    if not compare(user.password,user_db.password):
        raise HTTPException(status_code=403, detail=f"Invalid credentials")
    
    access_token = oauth2.create_access_token(data={'user_id':user_db.id})

    return {'access_token':access_token,'token_type':'bearer'}
    