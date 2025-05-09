import jwt
from app.models import User
from datetime import datetime, timedelta, UTC
from jwt.exceptions import ExpiredSignatureError
from sqlmodel import select
from app import schemas, models
from app.database import  get_db, Session
from fastapi import FastAPI, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
from app.config import settings


SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes

oaut2_scheme = OAuth2PasswordBearer(tokenUrl='login')

def create_access_token(data:str):
    to_encode = data.copy()
    expire = datetime.now(UTC) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({'exp':expire})
    encoded_jwt=jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM)
    return encoded_jwt

def verify_access_token(token:str, credential_exception):
    try:
        # print('Test')
        # print(f'Token:{token} key:{SECRET_KEY} algo:{ALGORITHM}')
        playload = jwt.decode(token, SECRET_KEY,algorithms=[ALGORITHM])
        # print('payload=',playload)
        id :int = playload.get('user_id')
        # print('id=',id)
        if id is None:
            raise credential_exception
        token_data = schemas.TokenData(id=id)
    except (ExpiredSignatureError,Exception) as e:
        print(e)
        print('Type: ',type(e))
        print('String of e',str(e))
        raise credential_exception
    return token_data
    
def get_current_user(token:str = Depends(oaut2_scheme), db:Session = Depends(get_db)):
    
    credential_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f'Could not validate credentials', headers={"WWW-Authenticate": "Bearer"})
    token = verify_access_token(token, credential_exception)
    user = db.exec(select(User).where(models.User.id ==token.id)).one_or_none()
    return user