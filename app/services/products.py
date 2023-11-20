from sqlalchemy.orm import Session
from fastapi import UploadFile
from sqlalchemy import func
from ..schemas.products import ProductCreate
from ..models.products import Product as ProductModel
from ..models.notices import Notice as NoticeModel
from ..models.users import User as UserModel
from ..models.likes import Like as LikeModel
from ..models.comments import Comment as CommentModel
from ..services.keywords import get_all_keywords
from ..image_db import upload_file


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
    if area and area != " ":
        query = query.filter(UserModel.activity_area.contains(area))
    if price_start:
        query = query.filter(ProductModel.price >= price_start)
    if price_end:
        query = query.filter(ProductModel.price <= price_end)

    return query.all()


def create_product(
    db: Session, product: ProductCreate, image: UploadFile, user_id: int
):
    try:
        db_product = ProductModel(**product.dict(), user_id=user_id)

        # 모든 키워드 정보 가져오기(User에 상관 없이)
        keywords = get_all_keywords(db)

        for keyword in keywords:
            # 각 키워드의 content 값이 product의 title에 포함되는지 확인
            # 자신의 키워드는 제외
            if (
                keyword.content.lower().strip() in db_product.title.lower().strip()
                and keyword.user_id != user_id
            ):
                # Notice 레코드 생성
                db_notice = NoticeModel(
                    user_id=keyword.user_id, keyword_id=keyword.keyword_id
                )
                db.add(db_notice)
                db.commit()
                db.refresh(db_notice)
                print("Notice 레코드 생성")

        # 이미지 파일 업로드
        file_url = upload_file("product/", image)
        db_product.image = file_url

        # Commit the entire transaction
        db.add(db_product)
        db.commit()
        db.refresh(db_product)

        return db_product

    except Exception as e:
        print(f"Error: {e}")
        db.rollback()
        raise


def get_product(db: Session, product_id: int):
    # Query for product details
    db_product = (
        db.query(ProductModel)
        .filter(ProductModel.product_id == product_id)
        .first()
    )

    if not db_product:
        return None

    # Query for like count
    like_count = (
        db.query(func.count(LikeModel.like_id))
        .filter(LikeModel.product_id == product_id)
        .scalar()
    )

    # Attach like_count to the product
    setattr(db_product, "like_count", like_count)

    return db_product



def like_product(db: Session, product_id: int, user_id: int):
    # 이미 좋아요를 눌렀는지 확인
    db_like = (
        db.query(LikeModel)
        .filter(LikeModel.product_id == product_id)
        .filter(LikeModel.user_id == user_id)
        .first()
    )
    if db_like:
        return None

    db_like = LikeModel(user_id=user_id, product_id=product_id)
    db.add(db_like)
    db.commit()
    db.refresh(db_like)

    # 업데이트 된 product 반환
    return get_product(db, product_id)


def get_selling_products(db: Session, user_id: int):
    return (
        db.query(ProductModel)
        .filter(ProductModel.user_id == user_id)
        .filter(ProductModel.is_sold.is_(False))
        .all()
    )


def get_liked_products(db: Session, user_id: int):
    return (
        db.query(ProductModel)
        .filter(ProductModel.is_sold.is_(False))
        .join(LikeModel, ProductModel.product_id == LikeModel.product_id)
        .filter(LikeModel.user_id == user_id)
        .all()
    )


def get_purchased_products(db: Session, user_id: int):
    return (
        db.query(ProductModel)
        .filter(ProductModel.is_sold.is_(True))
        .filter(ProductModel.user_id == user_id)
        .all()
    )


# 댓글 다는 기능
def register_commment_in_product(product_id, db, user_id, comment):
    # comment 객체 생성
    db_comment = CommentModel(
        content=comment, product_id=product_id, user_id=user_id
    )
    db.add(db_comment)
    db.commit()
    db.refresh(db_comment)
    
    return db_comment


# 모든 댓글 가져오기
def get_all_comments(product_id, db):
    
    return (
        db.query(CommentModel)
        .filter(CommentModel.product_id == product_id).all()
    )


# 게시글 전부 삭제하는 기능
def remove_product(user_id, db, current_user):
    # 관리자인 경우에만
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Permission denied. Only admin users can remove products."
        )   
    else:
        db.query(ProductModel).filter(ProductModel.user_id == user_id).delete()
        db.commit()
        return {"message": f"All products for user_id {user_id} deleted successfully"}