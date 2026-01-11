from sqlalchemy import Column, Integer, String, Date, Boolean, Enum, Text, Float, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base
import enum

class ContactCategoryDB(str, enum.Enum):
    FAMILY = "family"
    FRIEND = "friend"
    WORK = "work"
    OTHER = "other"

class Contact(Base):
    __tablename__ = "contacts"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    phone = Column(String(20), nullable=False)
    address = Column(String(200))
    category = Column(Enum(ContactCategoryDB), default=ContactCategoryDB.OTHER)
    birthday = Column(Date)
    notes = Column(Text)
    is_favorite = Column(Boolean, default=False)
    created_at = Column(Date, default=func.now())
    products = relationship("Product", back_populates="supplier", cascade="all, delete-orphan")

class Product(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    description = Column(Text)
    price = Column(Float, nullable=False)
    quantity = Column(Integer, default=0)
    created_at = Column(Date, default=func.now())
    supplier_id = Column(Integer, ForeignKey("contacts.id", ondelete="CASCADE"))
    supplier = relationship("Contact", back_populates="products")