from ..schemas import products as schema
from ..models.products import Product
from ..models.users import User
from sqlalchemy.orm import Session


def get_all_product(
    db: Session, title: str, area: str, price_start: int, price_end: int
):
    query = db.query(Product).join(User, Product.user_id == User.user_id)

    if title:
        query = query.filter(Product.title.contains(title))
    if area:
        query = query.filter(User.activity_area.contains(area))
    if price_start:
        query = query.filter(Product.price >= price_start)
    if price_end:
        query = query.filter(Product.price <= price_end)

    return query.all()


def create_product(db: Session, product: schema.ProductCreate, user_id: int):
    db_product = Product(**product.dict(), user_id=user_id)
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product


def get_product(db: Session, product_id: int):
    return db.query(Product).filter(Product.product_id == product_id).first()
