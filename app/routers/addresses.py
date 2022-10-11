"""
Module handling all the contacts endpoints for our address book api
"""

from fastapi import HTTPException,status,Response,Depends,APIRouter
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from app import models,schemas,oauth2
from app.database import get_db
from sqlalchemy.orm import Session
from typing import List
from geopy.geocoders import Nominatim
from geopy.distance import geodesic


router=APIRouter(
    prefix='/contacts',
    tags=['Contacts']
)


@router.get('/', status_code=status.HTTP_200_OK, response_model=List[schemas.ContactResponse])
def get_all_contacts(db: Session = Depends(get_db), current_user: schemas.TokenData = Depends(oauth2.get_current_user)):
    # getting all the contacts for the current logged in user and only those contacts from the database which have owner id same as 
    # current users id.
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
def create_contact(contact:schemas.BaseContact, db: Session = Depends(get_db), current_user: schemas.TokenData = Depends(oauth2.get_current_user)):
    # creating a new contact in the database

    contact_check=db.query(models.Contact).filter(models.Contact.email==contact.email).filter(models.Contact.owner_id == current_user.id).first()

    #checking if contact with the provided email already exists or not.
    if contact_check:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f'Contact with email id "{contact.email}" already exists in the address book.')

    # storing a string combined up from city,zipcode,country into address variable.
    address=contact.city+','+contact.zipcode+','+contact.country
    geolocator = Nominatim(user_agent="address-book-app")
    # fetching the location of the above address using geopy ( nominatim + geolocator) package
    location = geolocator.geocode(address)

    # Raising HTTP exception if the location of the address is not found because of some error in the input details 
    if location == None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Kindly check your address again and fill in correct inputs!")

    # if location is found accurately , store the contact in the database, also storing the latitude and longitude of the location found.
    new_contact=models.Contact(owner_id=current_user.id, latitude=location.latitude, longitude=location.longitude, **contact.dict())
    db.add(new_contact)
    db.commit()
    db.refresh(new_contact)

    return new_contact



@router.put('/{id}', status_code=status.HTTP_201_CREATED, response_model=schemas.ContactResponse)
def update_contact(id:int, contact_up: schemas.BaseContact, db: Session = Depends(get_db), current_user: schemas.TokenData = Depends(oauth2.get_current_user)):
    # updating the contact (user must be the owner else he/she can't perform the operation)

    found_contact_query = db.query(models.Contact).filter(models.Contact.id==id)
    contact = found_contact_query.first()
    if not contact:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Contact with ID {id} does not exist!!")
    
    if contact.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"You are unauthorized to update this contact...")

    # finding the location using geopy to find out the coordinates of the updates address
    address=contact_up.city+','+contact_up.zipcode+','+contact_up.country
    geolocator = Nominatim(user_agent="address-book-app")
    location = geolocator.geocode(address)

    if location == None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Kindly check your address again and fill in correct inputs!")

    # converting the pydantic model to dictionary
    updated_contact=contact_up.dict()
    # adding latitude and longitude coordinates as key in the updated_contact dictionary which will be actually updating our contact in the db.
    updated_contact['latitude']=location.latitude
    updated_contact['longitude']=location.longitude

    found_contact_query.update(updated_contact, synchronize_session=False)
    db.commit()

    return found_contact_query.first()



@router.delete('/{id}',status_code=status.HTTP_204_NO_CONTENT)
def delete_contact(id:int,db: Session = Depends(get_db), current_user: schemas.TokenData = Depends(oauth2.get_current_user) ):
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



@router.post('/retrieve/',response_model=List[schemas.ContactResponse])
def retrieve_contacts(own_location: schemas.RetreiveContacts, db: Session = Depends(get_db), current_user: schemas.TokenData = Depends(oauth2.get_current_user)):

    # to retrive addresses/contacts within given radius, first we will find out the current coordinates of the requestor
    current_address=own_location.current_city+','+own_location.current_zipcode+','+own_location.current_country
    geolocator = Nominatim(user_agent="address-book-app")
    location = geolocator.geocode(current_address)

    if location == None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Kindly check your address again and fill in correct inputs!")

    # once the location is found from above code, store the latitude and longitude as own_coordinates for the current location
    own_coordinates = (location.latitude, location.longitude)
    # defining a result_set list to store the contacts which we will fetch from queryset after checking their distance from own_coordinates.
    result_set = []
    contacts=db.query(models.Contact).filter(models.Contact.owner_id==current_user.id).all()
    
    # logic to loop over all the contacts returned by the queryset and calculate the distance between own and the contact's coordinates using geodesic. if distance is equal to or within the radius, we will append it to the result_Set
    for contact in contacts:
        contact_coordinates=(contact.latitude,contact.longitude)
        distance=geodesic(own_coordinates,contact_coordinates).km
        if distance <= own_location.radius_to_check_in_kms:
            result_set.append(contact)

    # if no contact found within a given radius, we will raise httpexception to let user know that nothing was found.
    if len(result_set) == 0:
        raise HTTPException(status_code=status.HTTP_200_OK, detail="No contacts within given radius, kindly extend the radius...")
    
    return result_set
    




