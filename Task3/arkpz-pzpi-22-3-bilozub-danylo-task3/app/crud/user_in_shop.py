from sqlalchemy.orm import Session
from app.models.user_in_shop import UserInShop
from app.schemas.user_in_shop import UserInShopCreate, UserInShopUpdate

def create_user_in_shop(db: Session, user_in_shop: UserInShopCreate):
    db_user_in_shop = UserInShop(**user_in_shop.dict())
    db.add(db_user_in_shop)
    db.commit()
    db.refresh(db_user_in_shop)
    return db_user_in_shop

def get_user_in_shop(db: Session, user_in_shop_id: int):
    return db.query(UserInShop).filter(UserInShop.user_in_shop_id == user_in_shop_id).first()

def get_users_in_shop(db: Session, skip: int = 0, limit: int = 100):
    return db.query(UserInShop).offset(skip).limit(limit).all()

def get_users_in_shop_by_shop_id(db: Session, shop_id: int):
    return db.query(UserInShop).filter(UserInShop.shop_id == shop_id).all()

def update_user_in_shop(db: Session, user_in_shop_id: int, user_in_shop: UserInShopUpdate):
    db_user_in_shop = db.query(UserInShop).filter(UserInShop.user_in_shop_id == user_in_shop_id).first()
    if db_user_in_shop:
        for key, value in user_in_shop.dict().items():
            setattr(db_user_in_shop, key, value)
        db.commit()
        db.refresh(db_user_in_shop)
    return db_user_in_shop

def delete_user_in_shop(db: Session, user_in_shop_id: int):
    db_user_in_shop = db.query(UserInShop).filter(UserInShop.user_in_shop_id == user_in_shop_id).first()
    if db_user_in_shop:
        db.delete(db_user_in_shop)
        db.commit()
    return db_user_in_shop
