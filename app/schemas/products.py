from pydantic import BaseModel
from .users import User


class ProductBase(BaseModel):
    title: str
    description: str
    price: int


class ProductCreate(ProductBase):
    pass


class Product(ProductBase):
    image: str
    product_id: int

    class Config:
        from_attribute = True


class ProductDetail(Product):
    owner: User
    is_sold: bool
    image: str
    like_count: int

    class Config:
        from_attribute = True
