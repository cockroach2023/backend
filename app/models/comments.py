from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
import datetime

from app.database import Base


class Comment(Base):
    __tablename__ = "comments"

    comment_id = Column(Integer, primary_key=True, index=True)

    content = Column(String(length=1024))
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    product_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id"))
