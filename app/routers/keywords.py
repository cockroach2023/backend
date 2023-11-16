from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..schemas.users import User
from typing import List
from ..schemas.keywords import KeywordRequest, KeywordResponse
from ..database import get_db
from ..utils.auth import get_current_user
from ..services import keywords as service

router = APIRouter()


# 관심 키워드 추가하기
@router.post("", response_model=KeywordResponse)
async def register_keyword(
    keyword: KeywordRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return service.register_keyword(db, keyword, current_user.user_id)


# 사용자 별 모든 키워드 가져오기
@router.get("", response_model=List[KeywordResponse])
async def get_all_keywords_by_user(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    keywords = service.get_all_keywords_by_user(db, current_user.user_id)
    print(keywords)
    return keywords


# 키워드 삭제하기
@router.delete("/{keyword_id}")
def delete_keyword(
    keyword_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    try:
        keyword = service.delete_keyword(
            db, keyword_id=keyword_id, user_id=current_user.user_id
        )
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

    return keyword
