from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship


from app.database import Base
from app.models.comments import Comment  # noqa
from app.models.likes import Like  # noqa


class Product(Base):
    __tablename__ = "products"

    product_id = Column(Integer, primary_key=True, index=True)
    title = Column(String(length=128))
    content = Column(String(length=1024))
    price = Column(Integer)
    description = Column(String(length=128))
    image = Column(String(length=128))

    user_id = Column(Integer, ForeignKey("users.user_id"))
    comments = relationship("Comment", back_populates="product")
    likes = relationship("Like", back_populates="product")

    owner = relationship("User", back_populates="products")
