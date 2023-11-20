from sqlalchemy import Column, ForeignKey, Integer, DateTime
import datetime
from sqlalchemy.orm import relationship



from app.database import Base


class Notice(Base):
    __tablename__ = "notices"

    notice_id = Column(Integer, primary_key=True, index=True)

    created_at = Column(DateTime, default=datetime.datetime.utcnow() + datetime.timedelta(hours=9))

    user_id = Column(Integer, ForeignKey("users.user_id"))
    keyword_id = Column(Integer, ForeignKey("keywords.keyword_id"))

    user = relationship("User", back_populates="notices")
    keywords = relationship("Keyword", back_populates="notices")
    