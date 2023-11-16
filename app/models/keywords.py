from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from app.database import Base


class Keyword(Base):
    __tablename__ = "keywords"

    keyword_id = Column(Integer, primary_key=True, index=True)
    content = Column(String(length=128))

    user_id = Column(Integer, ForeignKey("users.user_id"))

    user = relationship("User", back_populates="keywords")
    notices = relationship("Notice", back_populates="keywords")
