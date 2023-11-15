from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from ..schemas import products as schema
from ..schemas import users as User
from ..services import products as service
from ..database import get_db
from ..utils.auth import get_current_user

router = APIRouter()

ACCESS_TOKEN_EXPIRE_MINUTES = 30


@router.get("", response_model=List[schema.Product])
async def get_all_products(
    title: Optional[str] = None,
    area: Optional[str] = None,
    price_start: Optional[int] = None,
    price_end: Optional[int] = None,
    db: Session = Depends(get_db),
):
    return service.get_all_product(db, title, area, price_start, price_end)


@router.post("", response_model=schema.Product)
async def create_product(
    product: schema.ProductCreate,
    db: Session = Depends(get_db),
    current_user: User.User = Depends(get_current_user),
):
    return service.create_product(db, product, current_user.user_id)


@router.get("/{product_id}", response_model=schema.ProductDetail)
async def get_product(
    product_id: int,
    db: Session = Depends(get_db),
):
    product = service.get_product(db, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product
