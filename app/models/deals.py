from sqlalchemy import Boolean, Column, Integer, ForeignKey, DateTime
from sqlalchemy.orm import relationship
import datetime
from app.database import Base


class Deal(Base):
    __tablename__ = "deals"

    deal_id = Column(Integer, primary_key=True, index=True)
    accepted = Column(Boolean, default=False)

    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    buyer_id = Column(Integer, ForeignKey("users.user_id"))
    product_id = Column(Integer, ForeignKey("products.product_id"))

    buyer = relationship("User", back_populates="deals")
