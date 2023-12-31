from fastapi import HTTPException, UploadFile
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from typing import Optional
from ..schemas import users as schema
from ..schemas.keywords import KeywordRequest, KeywordResponse
from ..models import users as model
from ..models import keywords as keywords_model
from ..image_db import upload_file

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def signup_user(db: Session, user: schema.UserCreate, image: Optional[UploadFile]):
    user_dict = user.dict()
    # 비밀번호 암호화
    user_dict["password"] = pwd_context.hash(user_dict["password"])

    db_user = model.User(**user_dict)

    if image:
        file_url = upload_file("profile/", image)
    else:
        file_url = None

    db_user.profile = file_url
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user


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
def register_keyword(db: Session, keyword: KeywordRequest):
    db_user = db.query(model.User).filter(model.User.user_id == keyword.user_id).first()

    if db_user:
        new_keyword = keywords_model.Keyword(content=keyword.content, user=db_user)
        db.add(new_keyword)
        db.commit()
        db.refresh(db_user)
        return KeywordResponse(
            keyword_id=new_keyword.keyword_id, content=new_keyword.content
        )
    else:
        raise HTTPException(status_code=404, detail="User not found")


def convert_to_keyword_response(keyword):
    return KeywordResponse(keyword_id=keyword.keyword_id, content=keyword.content)


# 사용자 별 모든 키워드 가져오기
def get_all_keywords(db: Session, user_id: int):
    db_user = db.query(model.User).filter(model.User.user_id == user_id).first()

    if db_user:
        keywords = (
            db.query(keywords_model.Keyword)
            .filter(keywords_model.Keyword.user_id == user_id)
            .all()
        )
        return [convert_to_keyword_response(keyword) for keyword in keywords]
    else:
        raise HTTPException(status_code=404, detail="User not found")


# 키워드 삭제하기
def delete_keyword(db: Session, keyword_id: int):
    keyword = (
        db.query(keywords_model.Keyword)
        .filter(keywords_model.Keyword.keyword_id == keyword_id)
        .first()
    )
    if keyword:
        db.delete(keyword)
        db.commit()
        return {"message": "successfully deleted"}
    else:
        raise HTTPException(status_code=404, detail="Keyword not found")
    
    
    
# 모든 유저 가져오기
def get_all_user(db, username):
    if username == "admin":
        return db.query(model.User).all()
    

# 블랙리스트 등록하기
def register_blacklist(db, user_id, current_user):
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Permission denied. Only admin users can remove products."
        )
    else:
        user = db.query(model.User).filter(model.User.user_id == user_id).first()
        if user:
            user.is_blocked = True
            db.commit()
            return user
        else:
            raise HTTPException(status_code=404, detail="User not found")
    

# 블랙리스트 해제하기
def remove_blacklist(db, user_id, current_user):
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Permission denied. Only admin users can remove products."
        )
    else:
        user = db.query(model.User).filter(model.User.user_id == user_id).first()
        if user:
            user.is_blocked = False
            db.commit()
            return user
        else:
            raise HTTPException(status_code=404, detail="User not found")