from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..utils.auth import get_current_user
from ..services import deals as service
from ..schemas.users import User
from ..schemas.deals import Deal

router = APIRouter()


# 판매자가 구매 요청 목록 조회
@router.get("", response_model=list[Deal])
async def get_deals(
    db: Session = Depends(get_db), current_user: User = Depends(get_current_user)
):
    return service.get_deals(db, user_id=current_user.user_id)


# 구매자가 구매 요청
@router.post("", response_model=Deal)
async def register_keyword(
    product_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    try:
        return service.requset_deal(
            db, product_id=product_id, user_id=current_user.user_id
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


# 판매자가 구매 요청 수락
@router.patch("/{deal_id}/accept", response_model=Deal)
async def accept_deal(
    deal_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    try:
        return service.accept_deal(db, deal_id=deal_id, user_id=current_user.user_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
