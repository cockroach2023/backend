from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship


from app.database import Base


class Product(Base):
    __tablename__ = "users"

    product_id = Column(Integer, primary_key=True, index=True)
    title = Column(String(length=128))
    content = Column(String(length=1024))
    price = Column(Integer)
    description = Column(String(length=128))
    image = Column(String(length=128))

    user_id = Column(Integer, ForeignKey("users.user_id"))
    products = relationship("User", back_populates="products")
    comments = relationship("Comment", back_populates="product")
    likes = relationship("Like", back_populates="product")
