"""
Module handling all the user endpoints for our address book api to create a new user or fetch an existing one
"""

from fastapi import HTTPException,status,Depends,APIRouter
from app import models,schemas,utils
from sqlalchemy.orm import Session
from app.database import get_db

router=APIRouter(
    prefix='/users',
    tags=['Users']
)

@router.post("/",status_code=status.HTTP_201_CREATED,response_model=schemas.UserResponse)
def create_user(user:schemas.UserCreate, db: Session = Depends(get_db)):
    # creating a new user
    
    existing_user=db.query(models.User).filter(models.User.email==user.email).first()

    if existing_user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,detail=f"User with Email ID '{user.email}' already exists!")
    
    hashed_password = utils.hash(user.password)
    user.password=hashed_password
    new_user=models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return new_user

@router.get("/{id}",response_model=schemas.UserResponse)
def get_user(id:int, db: Session = Depends(get_db)):
    # getting an existing user with an id

    user=db.query(models.User).filter(models.User.id==id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"User with ID {id} does not exist!")
    
    return user

