from pydantic import BaseModel


class KeywordBase(BaseModel):
    content: str


class KeywordRequest(KeywordBase):
    class Config:
        from_attribute = True


class KeywordResponse(KeywordBase):
    keyword_id: int

    class Config:
        from_attribute = True


class Keyword(KeywordBase):
    keyword_id: int
    user_id: int

    class Config:
        from_attribute = True
