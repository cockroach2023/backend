from sqlalchemy import Column, Integer, ForeignKey, DateTime
from sqlalchemy.orm import relationship
import datetime
from app.database import Base


class Deal(Base):
    __tablename__ = "deals"

    deal_id = Column(Integer, primary_key=True, index=True)

    created_at = Column(DateTime, default=datetime.datetime.utcnow() + datetime.timedelta(hours=9))

    buyer_id = Column(Integer, ForeignKey("users.user_id"))
    product_id = Column(Integer, ForeignKey("products.product_id"))

    buyer = relationship("User", back_populates="deals")
    product = relationship("Product", back_populates="deals")
