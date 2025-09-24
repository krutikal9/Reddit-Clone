from fastapi import FastAPI, HTTPException, Response, status, Depends, APIRouter, Query
from app import models, schemas, oauth2,database
from app.database import  get_db, Session
from sqlmodel import select
from psycopg.errors import UniqueViolation, ForeignKeyViolation
from sqlalchemy.exc import IntegrityError
from app.models import RedditPost, Votes
from app.schemas import RedditPostResponseVotes
from sqlmodel import select, func
from typing import Optional, List



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

@router.get('',status_code=status.HTTP_200_OK,response_model=List[RedditPostResponseVotes])
def get_votes(db:Session = Depends(get_db),current_user:int =Depends(oauth2.get_current_user),search: Optional[str]='',offset: int = 0,limit:int=Query(default=99,le=100)):
    results = db.exec(select(RedditPost,func.count(Votes.redditposts_id).label('votes')).filter(RedditPost.content.contains(search)).offset(offset).limit(limit).join(Votes, isouter=True).group_by(RedditPost.id)).all()
    return results

@router.get('/{id}',status_code=status.HTTP_200_OK,response_model=Votes)
def get_votes(id:int,vote: schemas.Vote,db:Session = Depends(get_db),current_user:int =Depends(oauth2.get_current_user)):
    results = db.get(models.Votes,id)
    print(f'{results=}')
    return results