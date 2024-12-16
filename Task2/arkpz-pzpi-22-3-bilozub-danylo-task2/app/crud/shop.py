from sqlalchemy.orm import Session
from app.models.shop import Shop
from app.schemas.shop import ShopCreate, ShopUpdate

def create_shop(db: Session, shop: ShopCreate):
    db_shop = Shop(**shop.dict())
    db.add(db_shop)
    db.commit()
    db.refresh(db_shop)
    return db_shop

def get_shop(db: Session, shop_id: int):
    return db.query(Shop).filter(Shop.shop_id == shop_id).first()

def update_shop(db: Session, shop_id: int, shop: ShopUpdate):
    db_shop = db.query(Shop).filter(Shop.shop_id == shop_id).first()
    if db_shop:
        for key, value in shop.dict().items():
            setattr(db_shop, key, value)
        db.commit()
        db.refresh(db_shop)
    return db_shop

def delete_shop(db: Session, shop_id: int):
    db_shop = db.query(Shop).filter(Shop.shop_id == shop_id).first()
    if db_shop:
        db.delete(db_shop)
        db.commit()
    return db_shop
