from pydantic import BaseModel
from .users import User


class ProductBase(BaseModel):
    title: str
    description: str
    price: float
    image: str


class ProductCreate(ProductBase):
    pass


class Product(ProductBase):
    product_id: int

    class Config:
        from_attribute = True


class ProductDetail(Product):
    owner: User

    class Config:
        from_attribute = True
