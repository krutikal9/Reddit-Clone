from fastapi import FastAPI, HTTPException, Response, status, Depends, APIRouter
from app import models, schemas, oauth2,database
from app.database import  get_db, Session
from sqlmodel import select
from psycopg.errors import UniqueViolation, ForeignKeyViolation
from sqlalchemy.exc import IntegrityError

router =APIRouter(
    prefix='/votes',
    tags=['Votes']
)

@router.post('',status_code=status.HTTP_200_OK)
def create_vote(vote: schemas.Vote,db:Session = Depends(get_db),current_user:int =Depends(oauth2.get_current_user)):

    redditpost = db.get(models.RedditPost,vote.redditposts_id)
    print(str(redditpost))
    if not redditpost:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f'RedditPost with id {vote.redditposts_id} not found')
    new_vote = db.exec(select(models.Votes).filter(models.Votes.redditposts_id == vote.redditposts_id, models.Votes.user_id == current_user.id)).one_or_none()
    if not new_vote:
        add_vote = models.Votes(redditposts_id= vote.redditposts_id, user_id=current_user.id)
        db.add(add_vote)
        db.commit()
        return{'message':'Sucessfully added vote'}
    db.delete(new_vote)
    db.commit()
    return{'message':'Sucessfully removed vote'}
