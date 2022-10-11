"""
Main file 
"""

from fastapi import FastAPI
from app import models
from app.database import engine
from app.routers import addresses, auth, users

# below command is tied up with our database.py file via an engine and will create tables in our database (whichever db we have configured in database.py)
models.Base.metadata.create_all(bind=engine)

#creating an FastAPI instance
app=FastAPI()

@app.get('/')
def root():
    return {"message":"Welcome to the Address Book API. Add '/docs' to the url to reach to the Swagger Docs for testing and documentation, thanks!"}

# individual endpoints added inside ./routers for addresses, users and auth
app.include_router(addresses.router)
app.include_router(users.router)
app.include_router(auth.router)
