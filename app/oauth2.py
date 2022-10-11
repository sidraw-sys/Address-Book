"""
Handling Authentication 
"""

from jose import JWTError,jwt
from datetime import datetime,timedelta
from datetime import datetime,timedelta
from app import schemas,database,models
from fastapi import Depends,HTTPException,status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')

SECRET_KEY= "sndksncknsimcn12381hnsjcnscbbjsjdi882uklkasl"
ALGORITHM= 'HS256'
ACCESS_TOKEN_EXPIRE_MINUTES=30

def create_token(data:dict):
    #creating a token for logging in user

    to_encode = data.copy()
    expiration_time =  datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp":expiration_time})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt

def verify_token(token:str,credentials_exception):
    # verifying a JWT token

    try:
        payload=jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id=payload.get('User_ID')
        user_email=payload.get('Email')

        if user_id is None:
            raise credentials_exception
        if user_email is None:
            raise credentials_exception
    
        token_data=schemas.TokenData(id=user_id,email=user_email)

    except JWTError:
        raise credentials_exception

    return token_data

def get_current_user(token:str = Depends(oauth2_scheme),db: Session = Depends(database.get_db)):
    # this is a dependency we have created so that whenever a user tries to access any path operation where he is required to be authenticated
    # then using this dependency we can make sure if he is already logged in or not and also returns the user detail to that specific end point 

    credentials_exception=HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail=f'Could not validate credentials',headers={"WWW-Authenticate":"Bearer"})

    token = verify_token(token,credentials_exception)
    user = db.query(models.User).filter(models.User.id==token.id).first()
    return user