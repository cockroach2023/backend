from pydantic import BaseModel

class KeywordResponse(BaseModel):
    keyword_id: int
    content: str
    
class KeywordRequest(BaseModel):
    content: str
    user_id: int