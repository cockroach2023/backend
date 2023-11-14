from ..schemas import users as schema
from ..models import users as model
from sqlalchemy.orm import Session
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def signup_user(db: Session, user: schema.UserCreate):
    user_dict = user.dict()
    # 비밀번호 암호화
    user_dict["password"] = pwd_context.hash(user_dict["password"])

    db.user = model.User(**user_dict)

    db.add(db.user)
    db.commit()
    db.refresh(db.user)

    return db.user


def auth_user(db: Session, username: str, password: str):
    db_user = db.query(model.User).filter(model.User.username == username).first()
    # username이 존재하는지 확인
    if not db_user:
        return False

    # password가 일치하는지 확인
    if not pwd_context.verify(password, db_user.password):
        return False

    return db_user
