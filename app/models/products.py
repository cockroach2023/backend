from sqlalchemy import Column, ForeignKey, Integer, String, Boolean
from sqlalchemy.orm import relationship


from app.database import Base
from app.models.comments import Comment  # noqa
from app.models.likes import Like  # noqa


class Product(Base):
    __tablename__ = "products"

    product_id = Column(Integer, primary_key=True, index=True)
    title = Column(String(length=128))
    description = Column(String(length=128))
    price = Column(Integer)
    image = Column(String(length=128))
    is_sold = Column(Boolean, default=False)

    user_id = Column(Integer, ForeignKey("users.user_id"))
    comments = relationship("Comment", back_populates="product")
    likes = relationship("Like", back_populates="product")

    owner = relationship("User", back_populates="products")
    deals = relationship("Deal", back_populates="product")
