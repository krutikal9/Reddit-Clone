from app.schemas import RedditPostResponse, RedditPostCreate, RedditPostUpdate, RedditPostResponseVotes
from fastapi import  HTTPException,  status, Depends, APIRouter,Query
from typing import List, Optional
from app.database import  get_db, Session
from app.models import RedditPost, Votes
from sqlmodel import select, func
from app import oauth2

router =APIRouter(
    prefix='/redditposts',
    tags=['RedditPosts']
)

@router.get('/votes',status_code=status.HTTP_200_OK,response_model=List[RedditPostResponseVotes])
def get_votes(db:Session = Depends(get_db),current_user:int =Depends(oauth2.get_current_user),search: Optional[str]='',offset: int = 0,limit:int=Query(default=99,le=100)):
    results = db.exec(select(RedditPost,func.count(Votes.redditposts_id).label('votes')).filter(RedditPost.content.contains(search)).offset(offset).limit(limit).join(Votes, isouter=True).group_by(RedditPost.id)).all()

    return results
    
@router.get('',status_code=status.HTTP_200_OK,response_model=List[RedditPostResponse])
def get_redditposts(db:Session = Depends(get_db),current_user:int =Depends(oauth2.get_current_user),search: Optional[str]='',offset: int = 0,limit:int=Query(default=2,le=100)):
    redditposts = db.exec(select(RedditPost).filter(RedditPost.content.contains(search)).offset(offset).limit(limit)).all()
    print(RedditPost.content)
    print(RedditPost.content.contains(search))
    return redditposts

@router.post('',status_code=status.HTTP_201_CREATED,response_model=RedditPostResponse)
def create_redditposts(redditposts: RedditPostCreate,db:Session = Depends(get_db), current_user:int =Depends(oauth2.get_current_user)):
    redditposts_data = RedditPost(user_id=current_user.id,**redditposts.model_dump())
    print(current_user.email)
    db.add(redditposts_data)
    db.commit()
    db.refresh(redditposts_data)
    return redditposts_data

@router.get('/{id}',status_code=status.HTTP_200_OK,response_model=RedditPostResponse)
def get_redditposts(id:int,db:Session = Depends(get_db),current_user:int =Depends(oauth2.get_current_user)):
        redditposts = db.get(RedditPost,id)
        if not redditposts:
            raise HTTPException(status_code=404, detail=f"RedditPost with {id} not found")
        return redditposts

@router.delete('/{id}',status_code=status.HTTP_204_NO_CONTENT)
def delete_redditposts(id: int,db:Session = Depends(get_db),current_user:int =Depends(oauth2.get_current_user)):
        redditposts = db.get(RedditPost,id)
        if not redditposts:
            raise HTTPException(status_code=404, detail=f"RedditPost with {id} not found")
        if redditposts.user_id != current_user.id:
                print(redditposts.user_id)
                print(current_user.id)
                raise HTTPException(status_code=403,detail='Not authorised to perform action!')
        db.delete(redditposts)
        db.commit()
        return {'Deleted record':redditposts}

@router.patch('/{id}',response_model=RedditPostResponse)
def update_redditposts(id:int,redditposts:RedditPostUpdate,db:Session = Depends(get_db),current_user:int =Depends(oauth2.get_current_user)):
    redditposts_db = db.get(RedditPost,id)
    if not redditposts_db:
        raise HTTPException(status_code=404, detail=f"RedditPost with {id} not found")
   
    if redditposts_db.user_id != current_user.id:
        raise HTTPException(status_code=403,detail='Not authorised to perform action!')
    redditposts_data = redditposts.model_dump(exclude_unset=True)
    redditposts_db.sqlmodel_update(redditposts_data)
    db.add(redditposts_db)
    db.commit()
    db.refresh(redditposts_db)
    return redditposts_db