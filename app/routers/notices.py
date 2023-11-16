from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..utils.auth import get_current_user
from ..schemas.users import User
from ..services import notices as NoticeService
from typing import List
from ..schemas import notices as NoticeSchema
router = APIRouter()

# 사용자 별 알림 가져오기(SWR을 통해 비동기적으로 변화 감지)
@router.get("/", response_model=List[NoticeSchema.NoticeResponse])
async def get_notice_by_user(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return NoticeService.get_notice_by_user(db, current_user.user_id)