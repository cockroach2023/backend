from sqlalchemy import Column, ForeignKey, Integer

from app.database import Base


class Like(Base):
    __tablename__ = "likes"

    like_id = Column(Integer, primary_key=True, index=True)

    user_id = Column(Integer, ForeignKey("users.user_id"))
    product_id = Column(Integer, ForeignKey("products.product_id"))
