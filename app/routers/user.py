
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
from .. import models,schema,utils
from ..database import engine,get_db
from passlib.context import CryptContext
#########################################################################################


router=APIRouter(
    prefix='/users',
    tags=['User']
)

#To create an user
@router.post("/",status_code=status.HTTP_201_CREATED,response_model=schema.UserOut)
def create_user(user:schema.UserCreate, db: Session = Depends(get_db)):
    hashed_password=utils.hash(user.password)
    user.password=hashed_password
    new_user=models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user) #to return the result
    return new_user

#To read an user
@router.get('/{id}',response_model=schema.UserOut)
def get_user(id:int, db: Session = Depends(get_db)):
    user=db.query(models.User).filter(models.User.id==id).first()
    query=db.query(models.User).filter(models.User.id==id)
    print(query)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"User with id:{id} was not found")

    return user