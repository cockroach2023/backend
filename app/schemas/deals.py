from pydantic import BaseModel


class DealBase(BaseModel):
    product_id: int
    buyer_id: int


class Deal(DealBase):
    class Config:
        from_attribute = True
