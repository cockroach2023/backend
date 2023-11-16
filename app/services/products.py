from ..schemas.products import ProductCreate
from ..models.products import Product as ProductModel
from ..models.notices import Notice as NoticeModel
from ..models.keywords import Keyword as KeywordModel
from ..models.users import User as UserModel
from sqlalchemy.orm import Session
from ..services.keywords import get_all_keywords


def get_all_product(
    db: Session, title: str, area: str, price_start: int, price_end: int
):
    query = (
        db.query(ProductModel)
        .filter(ProductModel.is_sold.is_(False))
        .join(UserModel, ProductModel.user_id == UserModel.user_id)
    )

    if title:
        query = query.filter(ProductModel.title.contains(title))
    if area:
        query = query.filter(UserModel.activity_area.contains(area))
    if price_start:
        query = query.filter(ProductModel.price >= price_start)
    if price_end:
        query = query.filter(ProductModel.price <= price_end)

    return query.all()


def create_product(db: Session, product: ProductCreate, user_id: int):
    db_product = ProductModel(**product.dict(), user_id=user_id)
    
    # 모든 키워드 정보 가져오기(User에 상관 없이)
    keywords = get_all_keywords(db)
    

    # 각 키워드의 content 값이 product의 title에 포함되는지 확인
    for keyword in keywords:
        if keyword.content.lower() in db_product.title.lower():
            # Notice 레코드 생성
            db_notice = NoticeModel(user_id=user_id, keyword_id=keyword.keyword_id)
            db.add(db_notice)
    
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product


def get_product(db: Session, product_id: int):
    return db.query(ProductModel).filter(ProductModel.product_id == product_id).first()
