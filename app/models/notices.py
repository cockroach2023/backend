from sqlalchemy import Column, ForeignKey, Integer, DateTime
import datetime


from app.database import Base


class Notice(Base):
    __tablename__ = "notices"

    notice_id = Column(Integer, primary_key=True, index=True)

    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    user_id = Column(Integer, ForeignKey("users.user_id"))
    keyword_id = Column(Integer, ForeignKey("keywords.keyword_id"))
