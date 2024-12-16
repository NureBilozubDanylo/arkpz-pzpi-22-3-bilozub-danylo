
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.crud import shop as crud_shop
from app.models.user import User
from app.schemas.shop import Shop, ShopBase, ShopCreate, ShopUpdate
from app.dependencies import get_current_user, get_current_admin_user

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=Shop)
def create_shop(shop: ShopCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_admin_user)):
    return crud_shop.create_shop(db=db, shop=shop)

@router.get("/{shop_id}", response_model=Shop)
def read_shop(shop_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_shop = crud_shop.get_shop(db, shop_id=shop_id)
    if db_shop is None:
        raise HTTPException(status_code=404, detail="Shop not found")
    return db_shop

@router.put("/{shop_id}", response_model=Shop)
def update_shop(shop_id: int, shop: ShopUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_admin_user)):
    db_shop = crud_shop.update_shop(db, shop_id=shop_id, shop=shop)
    if db_shop is None:
        raise HTTPException(status_code=404, detail="Shop not found")
    return db_shop

@router.delete("/{shop_id}", response_model=Shop)
def delete_shop(shop_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_admin_user)):
    db_shop = crud_shop.delete_shop(db, shop_id=shop_id)
    if db_shop is None:
        raise HTTPException(status_code=404, detail="Shop not found")
    return db_shop