from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.crud import shop_supplies as crud_shop_supplies
from app.crud import notification as crud_notification
from app.crud import user_in_shop as crud_user_in_shop
from app.models.user import User
from app.schemas.shop_supplies import ShopSupplies, ShopSuppliesBase, ShopSuppliesCreate, ShopSuppliesUpdate, DeductSupply
from app.schemas.notification import NotificationCreate
from datetime import datetime
from app.dependencies import get_current_user, get_current_admin_user

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=ShopSupplies)
def create_shop_supplies(shop_supplies: ShopSuppliesCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_admin_user)):
    return crud_shop_supplies.create_shop_supplies(db=db, shop_supplies=shop_supplies)

@router.get("/{shop_supplies_id}", response_model=ShopSupplies)
def read_shop_supplies(shop_supplies_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_shop_supplies = crud_shop_supplies.get_shop_supplies(db, shop_supplies_id=shop_supplies_id)
    if db_shop_supplies is None:
        raise HTTPException(status_code=404, detail="Shop supplies not found")
    return db_shop_supplies

@router.put("/{shop_supplies_id}", response_model=ShopSupplies)
def update_shop_supplies(shop_supplies_id: int, shop_supplies: ShopSuppliesUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_admin_user)):
    db_shop_supplies = crud_shop_supplies.update_shop_supplies(db, shop_supplies_id=shop_supplies_id, shop_supplies=shop_supplies)
    if db_shop_supplies is None:
        raise HTTPException(status_code=404, detail="Shop supplies not found")
    return db_shop_supplies

@router.delete("/{shop_supplies_id}", response_model=ShopSupplies)
def delete_shop_supplies(shop_supplies_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_admin_user)):
    db_shop_supplies = crud_shop_supplies.delete_shop_supplies(db, shop_supplies_id=shop_supplies_id)
    if db_shop_supplies is None:
        raise HTTPException(status_code=404, detail="Shop supplies not found")
    return db_shop_supplies

@router.post("/deduct_supply", response_model=ShopSupplies)
def deduct_supply(shop_supplies: DeductSupply, db: Session = Depends(get_db), current_user: User = Depends(get_current_admin_user)):
    db_shop_supplies = crud_shop_supplies.get_shop_supplies_by_shop_and_supply(db, shop_id=shop_supplies.shop_id, supply_id=shop_supplies.supply_id)
    if db_shop_supplies is None:
        raise HTTPException(status_code=404, detail="Shop supplies not found")
    
    db_shop_supplies.quantity -= shop_supplies.quantity
    if db_shop_supplies.quantity < 0:
        db_shop_supplies.quantity = 0
    
    db.commit()
    db.refresh(db_shop_supplies)
    
    if db_shop_supplies.quantity <= 5:
        warning_message = f"Warning: Supply {shop_supplies.supply_id} in shop {shop_supplies.shop_id} is low (quantity: {db_shop_supplies.quantity})."
        print(warning_message)
        users_in_shop = crud_user_in_shop.get_users_in_shop_by_shop_id(db, shop_id=shop_supplies.shop_id)
        for user_in_shop in users_in_shop:
            notification = NotificationCreate(
                user_id=user_in_shop.user_id,
                message=warning_message,
                timestamp=datetime.now()
            )
            crud_notification.create_notification(db=db, notification=notification)
    
    return db_shop_supplies