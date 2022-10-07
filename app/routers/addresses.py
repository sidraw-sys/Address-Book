"""
Module handling all the contacts endpoints for our address book api
"""

from fastapi import HTTPException,status,Response,Depends,APIRouter
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from .. import models,schemas,oauth2
from ..database import get_db
from sqlalchemy.orm import Session
from typing import List
from geopy.distance import geodesic
from geopy.geocoders import Nominatim

router=APIRouter(
    prefix='/contacts',
    tags=['Contacts']
)

@router.get('/', status_code=status.HTTP_200_OK, response_model=List[schemas.ContactResponse])
def get_all_contacts(db: Session = Depends(get_db), current_user: schemas.TokenData = Depends(oauth2.get_current_user)):
    # getting all the contacts for the current logged in user and only those contacts from the database which have owner id same as current users id.
    contacts=db.query(models.Contact).filter(models.Contact.owner_id==current_user.id).all()

    return contacts

@router.get('/{id}',status_code=status.HTTP_200_OK, response_model=schemas.ContactResponse)
def get_single_contact(id:int,db: Session = Depends(get_db), current_user: schemas.TokenData = Depends(oauth2.get_current_user)):
    # get single contact with the specified id (user must be the owner of that contact)

    contact=db.query(models.Contact).filter(models.Contact.id==id).first()

    if not contact:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Contact with ID {id} does not exist!!")
    
    
    if contact.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"You are unauthorized to access this contact...")

    return contact
    

@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.ContactResponse)
def create_contact(contact:schemas.Contact, db: Session = Depends(get_db), current_user: schemas.TokenData = Depends(oauth2.get_current_user)):
    # creating a new contact in the databse

    new_contact=models.Contact(owner_id=current_user.id, **contact.dict())
    db.add(new_contact)
    db.commit()
    db.refresh(new_contact)

    return new_contact



@router.put('/{id}', status_code=status.HTTP_201_CREATED, response_model=schemas.ContactResponse)
def update_address(id:int, contact_m: schemas.Contact, db: Session = Depends(get_db), current_user: schemas.TokenData = Depends(oauth2.get_current_user)):
    # updating the contact (user must be the owner else he/she can't perform the operation)

    found_contact_query = db.query(models.Contact).filter(models.Contact.id==id)
    contact = found_contact_query.first()
    if not contact:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Contact with ID {id} does not exist!!")
    
    if contact.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"You are unauthorized to update this contact...")

    found_contact_query.update(contact_m.dict(), synchronize_session=False)
    db.commit()

    return found_contact_query.first()
    

@router.delete('/{id}',status_code=status.HTTP_204_NO_CONTENT)
def delete_address(id:int,db: Session = Depends(get_db), current_user: schemas.TokenData = Depends(oauth2.get_current_user) ):
    # deleting a contact (user must be the owner else he/she can't perform the operation)

    found_contact_query=db.query(models.Contact).filter(models.Contact.id==id)
    contact=found_contact_query.first()

    if not contact:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Contact with ID {id} does not exist!!")
    
    if contact.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"You are unauthorized to delete this contact...")

    found_contact_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

""" @router.post('/retrieve/')
def retrieve_addresses(data: schemas.RetreiveContacts, db: Session = Depends(get_db), current_user: schemas.TokenData = Depends(oauth2.get_current_user)):
    geolocator = Nominatim(user_agent="address-book")
    location = geolocator.geocode(data.own_location)
    own_latitude, own_longitude = location.latitude, location.longitude

    contacts=db.query(models.Contact).filter(models.Contact.owner_id==current_user.id).all() """

    




