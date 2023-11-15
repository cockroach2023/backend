from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from ..schemas import products as schema
from ..services import products as service
from ..database import get_db
from ..utils.auth import get_current_user

router = APIRouter()

ACCESS_TOKEN_EXPIRE_MINUTES = 30


@router.get("", response_model=List[schema.Product])
async def get_all_products(db: Session = Depends(get_db)):
    return service.get_all_product(db)


@router.post("", response_model=schema.Product)
async def create_product(
    product: schema.ProductCreate,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user),
):
    return service.create_product(db, product, current_user)


@router.get("/{product_id}")
async def get_product(
    product_id: int,
    db: Session = Depends(get_db),
):
    product = service.get_product(db, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product
