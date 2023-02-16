from fastapi import APIRouter,Depends,HTTPException,Response,status
from .. import database,schema,models,utils,oauth2
from sqlalchemy.orm import Session
from fastapi.security.oauth2 import OAuth2PasswordRequestForm

router=APIRouter(
    tags=(['Authentication'])
)

@router.post('/login',response_model=schema.Token)
def login(user_cradentials:OAuth2PasswordRequestForm=Depends(), db:Session=Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.email==user_cradentials.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail='Invalid Mail')
    
    if not utils.verify(user_cradentials.password,user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail='Invalid Password')
    access_token=oauth2.create_access_token(data={"user_id":user.id})
    return {'access_token':access_token,'token_type':'bearer'}
