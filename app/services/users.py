from ..schemas import users as schema
from ..models import users as model
from sqlalchemy.orm import Session


def signup_user(db: Session, user: schema.UserCreate):
    user_dict = user.dict()

    db.user = model.User(**user_dict)

    db.add(db.user)
    db.commit()
    db.refresh(db.user)

    return db.user


def login_user(db: Session, login: schema.UserLogin):
    print(login)
    db_user = db.query(model.User).filter(model.User.username == login.username).first()

    if db_user is None or db_user.password != login.password:
        return None

    return db_user
