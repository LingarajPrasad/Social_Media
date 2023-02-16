
#libraries
#########################################################################################
from fastapi import FastAPI,Response,status,HTTPException,Depends,APIRouter
from fastapi.params import Body
from typing import Optional,List
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from sqlalchemy.orm import Session
from sqlalchemy import func
from .. import models,schema,utils,oauth2
from ..database import engine,get_db
from passlib.context import CryptContext
#########################################################################################

router=APIRouter(
    prefix='/post',
    tags=['Posts']
)

#To get all posts
# {{URL}}post?Limit=2 in path
# {{URL}}post?Limit=3&skip=2 in path
@router.get("/",response_model=List[schema.PostOut])
def get_posts(db: Session = Depends(get_db),current_user:int=Depends(oauth2.get_current_user),Limit:int=10,skip:int=0,search:Optional[str]=''):
    # posts=db.query(models.Post).filter(models.Post.title.contains(search)).limit(Limit).offset(skip).all()
    result=db.query(models.Post,func.count(models.Vote.post_id).label('votes')).join(models.Vote, models.Vote.post_id==models.Post.id,isouter=True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(Limit).offset(skip).all()
    # print(result) you can print the query
    # print(current_user.email) logged in user
    return result

#To get all posts of one user
@router.get("/self",response_model=List[schema.Post])
def get_posts(
    db: Session = Depends(get_db),
    current_user:int=Depends(oauth2.get_current_user)
    ):
    posts=db.query(models.Post).filter(models.Post.owner_id==current_user.id).all()
    print(current_user.email)
    return posts

#To create a post
@router.post("/",status_code=status.HTTP_201_CREATED,response_model=schema.Post)
def create_posts(post:schema.PostCreate,db: Session = Depends(get_db),current_user:int=Depends(oauth2.get_current_user)):
    new_post=models.Post(owner_id=current_user.id,**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post) #to return the result
    return new_post

#To get a post by ID
@router.get("/{id}",response_model=schema.PostOut)
def get_post(id: int, db: Session = Depends(get_db),current_user:int=Depends(oauth2.get_current_user)):
    post=db.query(models.Post).filter(models.Post.id==id).first()
    post2=db.query(models.Post,func.count(models.Vote.post_id).label('votes')).join(models.Vote, models.Vote.post_id==models.Post.id,isouter=True).group_by(models.Post.id).filter(models.Post.id==id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id:{id} was not found")
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="It is not your post")
    return post2


#To delete a post
@router.delete("/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int,db: Session = Depends(get_db),current_user:int=Depends(oauth2.get_current_user)):
    post_query=db.query(models.Post).filter(models.Post.id==id)
    post=post_query.first()
    if post==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id:{id} was not found")
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="It is not your post")
    post_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


#to update a post
@router.put("/{id}",response_model=schema.Post)
def update_post(id:int, updates_post:schema.PostUpdate,db: Session = Depends(get_db),current_user:int=Depends(oauth2.get_current_user)):
    post_query=db.query(models.Post).filter(models.Post.id==id)
    post=post_query.first()
    if post==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id:{id} was not found")
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="It is not your post")
    post_query.update(updates_post.dict(),synchronize_session=False)
    db.commit()
    return post_query.first()