from app.schema import PostCreate, PostResponse, PostOut, Post
from fastapi import FastAPI, status, HTTPException, Response, Depends, APIRouter
from .. import models
from typing import Optional, List
from sqlalchemy.orm import Session
from .. utils import get_db, userdb
from . auth import get_the_current_user
from sqlalchemy import select, func
from ..models  import Vote

router = APIRouter(tags=["Post"])




@router.get("/get-posts", response_model=List[PostOut])
def get_post(db: Session = Depends(get_db), token_data = Depends(get_the_current_user), list: int | None = None, skip: int = 0, search: Optional[str] = ""):
    #post = db.query(models.Post).filter(models.Post.title.contains(search)).limit(list).offset(skip).all()
    result = db.query(models.Post, func.count(models.Vote.posts_id).label("votes")).join(models.Vote, models.Vote.posts_id == models.Post.id,
                                                                                           isouter=True).group_by(models.Post.id).filter(
                                                                                                 models.Post.title.contains(search)).limit(list).offset(skip).all()
          
    return result
    #cur.execute("""SELECT * FROM posts""")
    #posts = cur.fetchall()
    #return {"Data": posts}

@router.post("/posts", status_code=201, response_model =  PostResponse)
def create_post(post: PostCreate, db: Session = Depends(get_db), token_data =  Depends(get_the_current_user)):
    user = db.query(models.User).filter(models.User.username==token_data.username).first()
    new_post = models.Post(**post.dict())
    new_post.owner_id = user.id
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

      


    
    #cur.execute("""INSERT INTO posts(tittle, content, published) VALUES (%s, %s, %s) RETURNING * 
                              #""", (post.tittle, post.content, post.published) )
    #posted_data = cur.fetchone()
    #conn.commit()     
    #return {"data": posted_data}
  


@router.get("/get-posts-id/{id}", status_code=200, response_model= PostOut)
def get_post_id(id: int,  db: Session = Depends(get_db), token_data = Depends(get_the_current_user)):
        post = db.query(models.Post, func.count(models.Vote.posts_id).label("votes")).join(
               models.Vote, models.Vote.posts_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.id == id).first()
        if post is None:
              raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with ID {id} doesn't exist" )
        #db_user = db.query(models.User).filter(models.User.username == token_data.username).first()
        #if post.Post.owner_id != db_user.id:
                #raise HTTPException(status_code=status.HTTP_405_METHOD_NOT_ALLOWED, detail="Random user can't access this post")
        return post
       

            
        





        
    #cur.execute("""SELECT * FROM posts WHERE id = %s""", (str(id)))
    #retrieved_post = cur.fetchone()
    #if retrieved_post:
       #return {f"Post retrieved with ID {id}": retrieved_post}
    #else:
         #raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with ID {id} doesn't exist" )



@router.get("/latest-posts/", response_model= PostResponse)
def get_lastest_post(db: Session = Depends(get_db), token_data = Depends(get_the_current_user)):
    posts = db.query(models.Post).all()
    return posts[-1]
    #cur.execute("""SELECT * FROM posts""")
    #data = cur.fetchall()
    #return {"Latest_post":  data[-1]}
    
    
    

@router.delete("/delete-posts/{id}", status_code=410, response_model = PostResponse)
def delete_posts(id: int, db: Session = Depends(get_db), token_data =  Depends(get_the_current_user)):
            post = db.query(models.Post).filter(models.Post.id == id)
            post_data = post.first()
            if not post_data:
                  raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Could not delete post! because ID {id} doesn't exist" )
            user = db.query(models.User).filter(models.User.username == token_data.username).first()
            if user.id != post_data.owner_id:
                  raise HTTPException(status_code=status.HTTP_405_METHOD_NOT_ALLOWED, detail=f"This post can't be deleted by a random user")
            db.delete(post_data)
            db.commit()
            return post_data.__dict__
            #cur.execute(f""" DELETE FROM posts WHERE id = {id} RETURNING * """)
            #deleted_post = cur.fetchone()
            #conn.commit()
            #if deleted_post:
               #return {"Message: this post has been deleted": deleted_post}
            #raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Could not delete post! because ID {id} doesn't exist" )


            
@router.put("/update-posts/{id}", status_code=201, response_model= PostResponse)
def update_posts(id: int, post: PostCreate, db: Session = Depends(get_db), token_data = Depends(get_the_current_user)):
   db_user = db.query(models.Post).filter(models.Post.id == id)
   posts = db_user.first()
   if posts is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with ID {id} not found")
   users = db.query(models.User).filter(models.User.username == token_data.username).first()
   if users.id != posts.owner_id:
         raise HTTPException(status_code=status.HTTP_405_METHOD_NOT_ALLOWED, detail="Random user can't update this post")
   db_user.update(post.dict(), synchronize_session=False)
   #updated_response = PostResponse(**post.dict())
   db.commit()
   return db_user.first()

    #db.execute(update(models.Post).where(models.Post.id == id).values(title = post.title, content = post.content, published = post.published))
    #cur.execute("""UPDATE posts SET tittle = %s, content = %s, published=%s  WHERE id = %s RETURNING *""", (post.tittle, post.content, post.published, id))
    #conn.commit()
    #updated_post = cur.fetchone()
    #if updated_post:
        #return {"Updated post": updated_post}
    #raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with ID {id} not found")


