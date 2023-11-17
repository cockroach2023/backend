from pydantic import BaseModel
from .users import User
import datetime

class CommentBase(BaseModel):
    content: str
    
        
class Comment(CommentBase):
    comment_id: int
    created_at: datetime.datetime
    author: User
    class Config:
        from_attribute = True