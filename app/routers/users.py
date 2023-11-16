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
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/me", response_model=User)
async def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user
