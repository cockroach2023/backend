from ..schemas.keywords import KeywordRequest
from ..models.users import User as UserModel
from ..models.keywords import Keyword as KeywordModel
from sqlalchemy.orm import Session


# 키워드 등록 함수
def register_keyword(db: Session, keyword: KeywordRequest, user_id: int):
    db_keyword = KeywordModel(**keyword.dict(), user_id=user_id)
    db.add(db_keyword)
    db.commit()
    db.refresh(db_keyword)

    return db_keyword


# 사용자 별 모든 키워드 가져오기
def get_all_keywords_by_user(db: Session, user_id: int):
    return db.query(KeywordModel).filter(UserModel.user_id == user_id).all()

# 모든 키워드 가져오기
def get_all_keywords(db: Session):
    return db.query(KeywordModel).all()

# 키워드 삭제하기
def delete_keyword(db: Session, keyword_id: int, user_id: int):
    db_keyword = (
        db.query(KeywordModel)
        .filter(UserModel.user_id == user_id)
        .filter(KeywordModel.keyword_id == keyword_id)
        .first()
    )

    if not db_keyword:
        raise ValueError("Keyword not found")
    db.delete(db_keyword)
    db.commit()
    return db_keyword
