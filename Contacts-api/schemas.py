from pydantic import BaseModel, Field, validator, EmailStr
from typing import Optional
from datetime import date, datetime
import re
from enum import Enum


class ContactCategory(str, Enum):
    FAMILY = "family"
    FRIEND = "friend"
    WORK = "work"
    OTHER = "other"


class ContactBase(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    email: EmailStr = Field(...)
    phone: str = Field(...)
    address: Optional[str] = Field(None, max_length=200)
    category: ContactCategory = Field(ContactCategory.OTHER)
    birthday: Optional[date] = Field(None)
    notes: Optional[str] = Field(None, max_length=500)
    is_favorite: bool = Field(False)

    @validator('phone')
    def validate_phone_number(cls, v):
        phone_pattern = r'^(\+7|8)\d{10}$'
        cleaned = re.sub(r'[\s\-\(\)]', '', v)

        if not re.match(phone_pattern, cleaned):
            raise ValueError('Phone number must be in format +7XXXXXXXXXX or 8XXXXXXXXXX')

        if cleaned.startswith('8'):
            cleaned = '+7' + cleaned[1:]

        return cleaned

    @validator('birthday')
    def validate_birthday(cls, v):
        if v and v > date.today():
            raise ValueError('Birthday must be in the past')
        return v

    @validator('name')
    def validate_name_format(cls, v):
        parts = v.strip().split()
        if len(parts) < 2:
            raise ValueError('Name should contain at least first and last name')
        return v


class ContactCreate(ContactBase):
    pass


class ContactUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=2, max_length=100)
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    address: Optional[str] = Field(None, max_length=200)
    category: Optional[ContactCategory] = None
    birthday: Optional[date] = None
    notes: Optional[str] = Field(None, max_length=500)
    is_favorite: Optional[bool] = None


class ContactResponse(ContactBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


class ProductBase(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    description: Optional[str] = None
    price: float = Field(..., gt=0)
    quantity: int = Field(0, ge=0)


class ProductCreate(ProductBase):
    supplier_id: int


class ProductUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=2, max_length=100)
    description: Optional[str] = None
    price: Optional[float] = Field(None, gt=0)
    quantity: Optional[int] = Field(None, ge=0)
    supplier_id: Optional[int] = None


class ProductResponse(ProductBase):
    id: int
    supplier_id: int
    created_at: datetime

    class Config:
        from_attributes = True