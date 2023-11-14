from sqlalchemy import Boolean, Column, Integer, String
from sqlalchemy.orm import relationship

from app.database import Base
from app.models.products import Product  # noqa
from app.models.deals import Deal  # noqa
from app.models.comments import Comment  # noqa
from app.models.likes import Like  # noqa
from app.models.keywords import Keyword  # noqa


class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, index=True)
    username = Column(String(length=128), unique=True, index=True)
    password = Column(String(length=128))
    nickname = Column(String(length=128))
    activity_area = Column(String(length=128))
    profile = Column(String(length=1024))
    is_admin = Column(Boolean, default=False)
    is_blocked = Column(Boolean, default=False)

    products = relationship("Product", back_populates="owner")
    deals = relationship("Deal", back_populates="buyer")
    comments = relationship("Comment", back_populates="author")
    likes = relationship("Like", back_populates="user")
    keywords = relationship("Keyword", back_populates="user")
