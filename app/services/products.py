from sqlalchemy.orm import Session
from typing import Optional
from fastapi import UploadFile
from ..schemas.products import ProductCreate
from ..models.products import Product as ProductModel
from ..models.users import User as UserModel
from ..image_db import upload_file


def get_all_product(
    db: Session, title: str, area: str, price_start: int, price_end: int
):
    query = (
        db.query(ProductModel)
        .filter(ProductModel.is_sold.is_(False))
        .join(UserModel, ProductModel.user_id == UserModel.user_id)
    )

    if title:
        query = query.filter(ProductModel.title.contains(title))
    if area:
        query = query.filter(UserModel.activity_area.contains(area))
    if price_start:
        query = query.filter(ProductModel.price >= price_start)
    if price_end:
        query = query.filter(ProductModel.price <= price_end)

    return query.all()


def create_product(
    db: Session, product: ProductCreate, image: Optional[UploadFile], user_id: int
):
    db_product = ProductModel(**product.dict(), user_id=user_id)
    file_url = upload_file("product/", image)
    db_product.image = file_url
    db.add(db_product)
    db.commit()
    db.refresh(db_product)

    return db_product


def get_product(db: Session, product_id: int):
    return db.query(ProductModel).filter(ProductModel.product_id == product_id).first()
