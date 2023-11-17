from pydantic import BaseModel
from .users import UserDeal
from .products import Product
import datetime


class DealBase(BaseModel):
    deal_id: int
    product_id: int
    buyer_id: int
    created_at: datetime.datetime


class Deal(DealBase):
    buyer: UserDeal
    product: Product

    class Config:
        from_attribute = True
