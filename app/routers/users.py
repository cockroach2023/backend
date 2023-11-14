from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Annotated
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta
from ..schemas import users as schema
from ..schemas import tokens as token
from ..services import users as service
from ..database import get_db
from ..utils.auth import create_access_token, get_current_user

router = APIRouter()

ACCESS_TOKEN_EXPIRE_MINUTES = 30


@router.post("/signup", response_model=schema.User)
def signup_user(user: schema.UserCreate, db: Session = Depends(get_db)):
    return service.signup_user(db, user)


@router.post("/login", response_model=token.Token)
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


@router.get("/me")
async def read_users_me(current_user: str = Depends(get_current_user)):
    return {"username": current_user}
