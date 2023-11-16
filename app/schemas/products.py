from pydantic import BaseModel
from .users import User
from typing import Optional


class ProductBase(BaseModel):
    title: str
    description: str
    price: int


class ProductCreate(ProductBase):
    pass


class Product(ProductBase):
    image: Optional[str]
    product_id: int

    class Config:
        from_attribute = True


class ProductDetail(Product):
    owner: User
    is_sold: bool
    image: str

    class Config:
        from_attribute = True
