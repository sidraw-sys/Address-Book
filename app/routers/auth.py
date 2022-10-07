"""
Module handling logging in for the user
"""

from fastapi import HTTPException,status,Response,Depends,APIRouter
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from .. import models,schemas,database,utils,oauth2
from sqlalchemy.orm import Session


router=APIRouter(tags=["Authentication"])


@router.post("/login",response_model=schemas.Token)
def login(user_Credentials:OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    # logging in user by verifying email and the already stored hashed password

    found_user=db.query(models.User).filter(models.User.email==user_Credentials.username).first()
    if not found_user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail=f'Invalid Credentials!')
    
    if not utils.verify(user_Credentials.password,found_user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail=f'Invalid Credentials!')
    
    access_token = oauth2.create_token(data = {"User_ID":found_user.id,"Email":found_user.email})

    return {"access_token":access_token,"token_type":"bearer"}
 
