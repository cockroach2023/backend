from pydantic import BaseModel
import datetime

class NoticeResponse(BaseModel):
    notice_id: int
    keyword_content: str
    created_at: datetime.datetime
    
    class Config:
        from_attributes=True