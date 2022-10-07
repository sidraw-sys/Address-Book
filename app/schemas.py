"""
Schema models used inside our endpoints for validation of the data being sent in POST requests and data coming in JSON responses from our API 
"""

from pydantic import BaseModel, EmailStr
from datetime import datetime

class UserCreate(BaseModel):
    # schema model to be followed while creating user
    email:EmailStr
    password:str

class UserResponse(BaseModel):
    # schema model to be followed while fetching the user info
    id:int
    email:EmailStr
    created_at: datetime

    class Config:
        orm_mode = True

class Contact(BaseModel):
    # schema model to be followed while creating contact
    f_name:str
    l_name:str
    email:str
    phone:str
    address:str
    city:str
    state:str
    zipcode:str
    

class ContactResponse(BaseModel):
    # schema model to be followed while fetching the contact from API
    id:int
    f_name:str
    l_name:str
    email:str
    phone:str
    address:str
    city:str
    state:str
    zipcode:str
    created_at:datetime
    owner_id:int

    class Config:
        orm_mode = True
    
class UserLogin(BaseModel):
    # schema model to be followed while logging in a user
    email:EmailStr
    password:str

class Token(BaseModel):
    # token schema for validating token when user tries to access the endpoints which require authentication
    access_token:str
    token_type:str

class TokenData(BaseModel):
    # schema to be followed while creating a token which is automatically handled in auth.py and oauth2.py
    id:int
    email:EmailStr

class RetreiveContacts(BaseModel):
    # schema model to retreive contacts within a given distance range.
    distance:int
    own_location:str 