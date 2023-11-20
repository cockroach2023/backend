from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session
from typing import Annotated
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta
from ..schemas.users import User, UserCreate
from ..schemas.tokens import Token
from ..services import users as service
from ..database import get_db
from ..utils.auth import create_access_token, get_current_user
from typing import List
router = APIRouter()

ACCESS_TOKEN_EXPIRE_MINUTES = 30


@router.post("/signup", response_model=User)
def signup_user(
    username: Annotated[str, Form()],
    password: Annotated[str, Form()],
    nickname: Annotated[str, Form()],
    activity_area: Annotated[str, Form()],
    db: Session = Depends(get_db),
    profile: UploadFile = File(None),
):
    try:
        user = UserCreate(
            username=username,
            password=password,
            nickname=nickname,
            activity_area=activity_area,
        )
    except Exception as e:
        raise HTTPException(status_code=422, detail=str(e))

    return service.signup_user(db, user, profile)


@router.post("/login", response_model=Token)
async def login_user(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Session = Depends(get_db),
):
    user = service.auth_user(db, form_data.username, form_data.password)

    if not user:
        raise HTTPException(
            status_code=404,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
    )
    if user.is_blocked:
        raise HTTPException(
            status_code=403,
            detail="user is blocked",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/me", response_model=User)
async def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user

# 모든 유저 조회
@router.get("/all-user", response_model=List[User])
async def get_all_user(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return service.get_all_user(db, current_user.username)

# 블랙리스트 등록
@router.post("/register/blacklist", response_model=User)
async def register_blacklist(user_id : int ,db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return service.register_blacklist(db, user_id, current_user)


# 블랙리스트 해제
@router.post("/remove/blacklist", response_model=User)
async def register_blacklist(user_id : int ,db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return service.remove_blacklist(db, user_id, current_user)