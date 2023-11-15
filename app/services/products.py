from ..schemas import products as schema
from ..models import products as model
from sqlalchemy.orm import Session


def get_all_product(db: Session):
    return db.query(model.Product).all()


def create_product(db: Session, product: schema.ProductCreate, current_user: str):
    db_product = model.Product(**product.dict(), user_id=current_user)
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product


def get_product(db: Session, product_id: int):
    return (
        db.query(model.Product).filter(model.Product.product_id == product_id).first()
    )
