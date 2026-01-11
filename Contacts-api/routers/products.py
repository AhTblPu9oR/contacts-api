from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from database import get_db
from models import Product, Contact

router = APIRouter(prefix="/products", tags=["products"])


@router.get("/")
def get_products(
        skip: int = Query(0, ge=0),
        limit: int = Query(10, ge=1, le=100),
        supplier_id: Optional[int] = None,
        db: Session = Depends(get_db)
):
    query = db.query(Product)
    if supplier_id:
        query = query.filter(Product.supplier_id == supplier_id)
    return query.offset(skip).limit(limit).all()


@router.post("/")
def create_product(
        name: str,
        price: float,
        supplier_id: int,
        description: Optional[str] = None,
        quantity: int = 0,
        db: Session = Depends(get_db)
):
    contact = db.query(Contact).filter(Contact.id == supplier_id).first()
    if not contact:
        raise HTTPException(status_code=404, detail="Contact not found")

    product = Product(
        name=name,
        price=price,
        description=description,
        quantity=quantity,
        supplier_id=supplier_id
    )

    db.add(product)
    db.commit()
    db.refresh(product)
    return product