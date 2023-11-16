from sqlalchemy.orm import Session
from ..services.products import get_product
from ..models.deals import Deal as DealModel


def requset_deal(
    db: Session,
    product_id: int,
    user_id: int,
):
    product = get_product(db, product_id)

    if not product:
        raise ValueError("Product not found")

    if product.owner.user_id == user_id:
        raise ValueError("You can't request deal to your product")

    deal = (
        db.query(DealModel)
        .filter(DealModel.product_id == product_id)
        .filter(DealModel.buyer_id == user_id)
        .first()
    )

    if deal:
        raise ValueError("You already requested deal")

    new_deal = DealModel(product_id=product_id, buyer_id=user_id)

    db.add(new_deal)
    db.commit()
    db.refresh(new_deal)

    return new_deal


def get_deals(db: Session, user_id: int):
    return db.query(DealModel).filter(DealModel.product.has(user_id=user_id)).all()
