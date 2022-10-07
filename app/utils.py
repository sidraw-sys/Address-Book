"""
Module containing the functions to hash the password and verifying the password while user is logging in.
"""

from passlib.context import CryptContext

pwd_context=CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash(password:str):
    """
    returns the hashed password which we store in database from inside of our endpoints.
    """
    return pwd_context.hash(password)

def verify(plain_password,hashed_password):
    """
    verifies the plain password which user have inserted for login against the already stored hashed password inside of the databse.
    """
    return pwd_context.verify(plain_password,hashed_password)