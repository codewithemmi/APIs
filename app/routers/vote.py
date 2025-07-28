from fastapi import APIRouter, Depends, status, HTTPException
from . auth import get_the_current_user
from .. main import Session
from .. utils import get_db
from . post import get_post
from .. import models
from typing import List
from .. schema import Vote
from sqlalchemy.orm.exc import UnmappedInstanceError
from sqlalchemy.exc import IntegrityError
from jwt.exceptions import ExpiredSignatureError



router =  APIRouter(tags=["Vote"])



@router.post("/vote")
def users_vote(vote: Vote, db: Session = Depends(get_db), token_data = Depends(get_the_current_user)):
    
    try: 

        user = db.query(models.User).filter(models.User.username == token_data.username).first()
        if vote.vote_dir == 0:
            data = db.query(models.Vote).filter(models.Vote.posts_id == vote.post_id, models.Vote.users_id == user.id).first()
            db.delete(data)
            db.commit()
            raise HTTPException(status_code=status.HTTP_410_GONE, detail='You have unvote this post')
        elif vote.vote_dir != 0:
            user_vote = db.query(models.Post).filter(models.Post.id == vote.post_id).first()
            if user_vote is None:
               raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"vote with post id {vote.post_id} doesn't exist" )
            else: 
                user_vote = models.Vote(posts_id = vote.post_id, users_id = user.id)
                db.add(user_vote)
                db.commit()
            raise HTTPException(status_code=status.HTTP_201_CREATED, detail="Voting this post was successfuly")
    except IntegrityError:
        raise HTTPException(status_code=status.HTTP_302_FOUND, detail="can't vote for same post twice")
    except UnmappedInstanceError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"vote with post id {vote.post_id} doesn't exist" )
    




        


    

    
    
    




    

