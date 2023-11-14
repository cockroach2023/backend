from sqlalchemy import Column, ForeignKey, Integer
from sqlalchemy.orm import relationship
from app.database import Base


class Like(Base):
    __tablename__ = "likes"

    like_id = Column(Integer, primary_key=True, index=True)

    user_id = Column(Integer, ForeignKey("users.user_id"))
    product_id = Column(Integer, ForeignKey("products.product_id"))

    product = relationship("Product", back_populates="likes")
    user = relationship("User", back_populates="likes")
