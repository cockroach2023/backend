from ..schemas import users as schema
from ..schemas import keyword as keyword_schema
from ..models import users as model
from ..models import keywords as keywords_model
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from fastapi import HTTPException
from typing import List

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


def get_user(db: Session, username: str):
    return db.query(model.User).filter(model.User.username == username).first()


# 키워드 등록 함수
def register_keyword(db: Session, keyword_request:keyword_schema.KeywordRequest):
    db_user = db.query(model.User).filter(model.User.user_id == keyword_request.user_id).first()
    
    if db_user:
        new_keyword = keywords_model.Keyword(content=keyword_request.content, user=db_user)
        db.add(new_keyword)
        db.commit()
        db.refresh(db_user)
        return keyword_schema.KeywordResponse(keyword_id=new_keyword.keyword_id, content=new_keyword.content)
    else:
        raise HTTPException(status_code=404, detail="User not found")


def convert_to_keyword_response(keyword):
    return keyword_schema.KeywordResponse(keyword_id=keyword.keyword_id, content=keyword.content)


# 사용자 별 모든 키워드 가져오기
def get_all_keywords(db: Session, user_id: int):
    db_user = db.query(model.User).filter(model.User.user_id == user_id).first()
    
    if db_user:
        keywords = db.query(keywords_model.Keyword).filter(keywords_model.Keyword.user_id == user_id).all()
        return [convert_to_keyword_response(keyword) for keyword in keywords]
    else:
        raise HTTPException(status_code=404, detail="User not found")
    
    
# 키워드 삭제하기
def delete_keyword(db: Session, keyword_id: int):
   keyword = db.query(keywords_model.Keyword).filter(keywords_model.Keyword.keyword_id == keyword_id).first()
   if keyword:
       db.delete(keyword)
       db.commit()
       return {"message": "successfully deleted"}
   else:
        raise HTTPException(status_code=404, detail="Keyword not found")