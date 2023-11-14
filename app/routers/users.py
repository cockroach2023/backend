from fastapi import APIRouter, Depends, HTTPException
from ..schemas import users as schema
from ..services import users as service
from ..database import get_db
from sqlalchemy.orm import Session

router = APIRouter()


@router.post("/signup", response_model=schema.User)
def signup_user(user: schema.UserCreate, db: Session = Depends(get_db)):
    return service.signup_user(db, user)


@router.post("/login", response_model=schema.User)
def login_user(user: schema.UserLogin, db: Session = Depends(get_db)):
    db_user = service.login_user(db, user)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user
