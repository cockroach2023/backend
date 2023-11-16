from ..models.notices import Notice as NoticeModel
from ..models.keywords import Keyword as KeywordModel
from sqlalchemy.orm import Session
from ..schemas.notices import NoticeResponse

# 유저 별 Notice 가져오기
def get_notice_by_user(db: Session, user_id: int):
    notice_list = db.query(NoticeModel).filter(NoticeModel.user_id == user_id).all()

    notice_response_list = []
    for notice in notice_list:
        
        keyword = db.query(KeywordModel).filter(KeywordModel.keyword_id==notice.keyword_id).first()

        keyword_content = keyword.content
        
        notice_response = NoticeResponse(
            notice_id=notice.notice_id,
            created_at=notice.created_at,
            keyword_content=keyword_content 
        )
        
        notice_response_list.append(notice_response)
    
    return notice_response_list
    