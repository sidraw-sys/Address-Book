"""
Tables created inside the database.
"""

from sqlalchemy import Column, Integer, String, ForeignKey, Float,DateTime
from app.database import Base
from sqlalchemy.sql import func
from sqlalchemy.sql.expression import text

class Contact(Base):
    __tablename__ ='contacts'


    id=Column(Integer,primary_key=True,nullable=False)
    f_name=Column(String,nullable=False)
    l_name=Column(String,nullable=False)
    email=Column(String,nullable=False)
    phone=Column(String,nullable=False)
    address=Column(String,nullable=False)
    city=Column(String,nullable=False)
    state=Column(String,nullable=False)
    zipcode=Column(String,nullable=False)
    country=Column(String,nullable=False)
    time_created = Column(DateTime(timezone=True), server_default=func.now())
    
    # will store latitude and longitude from the provided address details, logic written in Path operations (routers/addresses.py)
    latitude=Column(Float,nullable=False)
    longitude=Column(Float,nullable=False)

    # Foreign key specifying relationship with the User model.
    owner_id=Column(Integer,ForeignKey("users.id",ondelete="CASCADE"),nullable=False)


class User(Base):
    __tablename__='users'

    id=Column(Integer,primary_key=True,nullable=False)
    email=Column(String,nullable=False,unique=True)
    password=Column(String,nullable=False)
    time_created = Column(DateTime(timezone=True), server_default=func.now())