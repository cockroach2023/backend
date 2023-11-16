from pydantic import BaseModel
import datetime


class DealBase(BaseModel):
    deal_id: int
    product_id: int
    buyer_id: int
    created_at: datetime.datetime


class Deal(DealBase):
    class Config:
        from_attribute = True
