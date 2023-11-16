from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session
from typing import List, Optional, Annotated
from ..schemas.products import ProductCreate, Product, ProductDetail
from ..schemas.users import User
from ..services import products as service
from ..database import get_db
from ..utils.auth import get_current_user

router = APIRouter()

ACCESS_TOKEN_EXPIRE_MINUTES = 30


@router.get("", response_model=List[Product])
async def get_all_products(
    title: Optional[str] = None,
    area: Optional[str] = None,
    price_start: Optional[int] = None,
    price_end: Optional[int] = None,
    db: Session = Depends(get_db),
):
    return service.get_all_product(db, title, area, price_start, price_end)


@router.post("", response_model=Product)
async def create_product(
    title: Annotated[str, Form()],
    description: Annotated[str, Form()],
    price: Annotated[int, Form()],
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    image: UploadFile = File(...),
):
    if image.content_type not in ["image/jpeg", "image/png"]:
        raise HTTPException(status_code=415, detail="File must be an image")

    try:
        product = ProductCreate(title=title, description=description, price=price)
    except Exception as e:
        raise HTTPException(status_code=422, detail=str(e))

    return service.create_product(db, product, image, current_user.user_id)


@router.get("/{product_id}", response_model=ProductDetail)
async def get_product(
    product_id: int,
    db: Session = Depends(get_db),
):
    product = service.get_product(db, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product


@router.post("/{product_id}/like", response_model=ProductDetail)
async def like_product(
    product_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    product = service.get_product(db, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    product = service.like_product(db, product_id, current_user.user_id)
    if not product:
        raise HTTPException(status_code=409, detail="Already liked")
    return product


@router.get("/user/selling", response_model=list[Product])
async def get_selling_products(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return service.get_selling_products(db, current_user.user_id)


@router.get("/user/liked", response_model=list[Product])
async def get_liked_products(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return service.get_liked_products(db, current_user.user_id)


@router.get("/user/purchased", response_model=list[Product])
async def get_purchased_products(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return service.get_purchased_products(db, current_user.user_id)
