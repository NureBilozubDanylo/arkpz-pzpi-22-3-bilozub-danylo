from sqlalchemy.orm import Session
from app.models.shop_supplies import ShopSupplies
from app.schemas.shop_supplies import ShopSuppliesCreate, ShopSuppliesUpdate

def create_shop_supplies(db: Session, shop_supplies: ShopSuppliesCreate):
    db_shop_supplies = ShopSupplies(**shop_supplies.dict())
    db.add(db_shop_supplies)
    db.commit()
    db.refresh(db_shop_supplies)
    return db_shop_supplies

def get_shop_supplies(db: Session, shop_supplies_id: int):
    return db.query(ShopSupplies).filter(ShopSupplies.shop_supplies_id == shop_supplies_id).first()

def get_all_shop_supplies(db: Session, skip: int = 0, limit: int = 100):
    return db.query(ShopSupplies).offset(skip).limit(limit).all()

def update_shop_supplies(db: Session, shop_supplies_id: int, shop_supplies: ShopSuppliesUpdate):
    db_shop_supplies = db.query(ShopSupplies).filter(ShopSupplies.shop_supplies_id == shop_supplies_id).first()
    if db_shop_supplies:
        for key, value in shop_supplies.dict().items():
            setattr(db_shop_supplies, key, value)
        db.commit()
        db.refresh(db_shop_supplies)
    return db_shop_supplies

def delete_shop_supplies(db: Session, shop_supplies_id: int):
    db_shop_supplies = db.query(ShopSupplies).filter(ShopSupplies.shop_supplies_id == shop_supplies_id).first()
    if db_shop_supplies:
        db.delete(db_shop_supplies)
        db.commit()
    return db_shop_supplies

def get_shop_supplies_by_shop_and_supply(db: Session, shop_id: int, supply_id: int):
    return db.query(ShopSupplies).filter(ShopSupplies.shop_id == shop_id, ShopSupplies.supply_id == supply_id).first()