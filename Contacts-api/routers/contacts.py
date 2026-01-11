from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from typing import List, Optional

from database import get_db
from models import Contact
from schemas import ContactCreate, ContactUpdate, ContactResponse, ContactCategory
router = APIRouter(prefix="/contacts", tags=["contacts"])


@router.post("/", response_model=ContactResponse, status_code=201)
def create_contact(contact: ContactCreate):
    try:
        return contacts_db.create_contact(contact)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/", response_model=List[ContactResponse])
def get_contacts(
        category: Optional[ContactCategory] = Query(None),
        favorite: Optional[bool] = Query(None),
        search: Optional[str] = Query(None),
        skip: int = Query(0, ge=0),
        limit: int = Query(100, ge=1, le=1000)
):
    contacts = contacts_db.get_all_contacts()

    if category:
        contacts = [c for c in contacts if c.category == category]

    if favorite is not None:
        contacts = [c for c in contacts if c.is_favorite == favorite]

    if search:
        contacts = contacts_db.search_contacts(search)

    return contacts[skip:skip + limit]


@router.get("/{contact_id}", response_model=ContactResponse)
def get_contact(contact_id: int):
    contact = contacts_db.get_contact(contact_id)
    if contact is None:
        raise HTTPException(status_code=404, detail="Contact not found")
    return contact


@router.put("/{contact_id}", response_model=ContactResponse)
def update_contact(contact_id: int, contact_update: ContactUpdate):
    update_data = contact_update.dict(exclude_unset=True)

    try:
        contact = contacts_db.update_contact(contact_id, update_data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    if contact is None:
        raise HTTPException(status_code=404, detail="Contact not found")

    return contact


@router.delete("/{contact_id}", status_code=204)
def delete_contact(contact_id: int):
    if not contacts_db.delete_contact(contact_id):
        raise HTTPException(status_code=404, detail="Contact not found")
    return None


@router.get("/birthday/upcoming", response_model=List[ContactResponse])
def get_upcoming_birthdays(days: int = Query(30, ge=1, le=365)):
    import datetime

    today = datetime.date.today()
    contacts = contacts_db.get_all_contacts()
    upcoming = []

    for contact in contacts:
        if contact.birthday:
            next_birthday = contact.birthday.replace(year=today.year)
            if next_birthday < today:
                next_birthday = next_birthday.replace(year=today.year + 1)

            days_until = (next_birthday - today).days
            if 0 <= days_until <= days:
                upcoming.append(contact)

    return upcoming