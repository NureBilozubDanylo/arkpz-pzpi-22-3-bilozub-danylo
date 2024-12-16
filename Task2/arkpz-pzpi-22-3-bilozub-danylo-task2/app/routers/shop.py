
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.crud import shop as crud_shop
from app.schemas.shop import ShopBase, ShopCreate, ShopUpdate

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=ShopBase)
def create_shop(shop: ShopCreate, db: Session = Depends(get_db)):
    return crud_shop.create_shop(db=db, shop=shop)

@router.get("/{shop_id}", response_model=ShopBase)
def read_shop(shop_id: int, db: Session = Depends(get_db)):
    db_shop = crud_shop.get_shop(db, shop_id=shop_id)
    if db_shop is None:
        raise HTTPException(status_code=404, detail="Shop not found")
    return db_shop

@router.put("/{shop_id}", response_model=ShopBase)
def update_shop(shop_id: int, shop: ShopUpdate, db: Session = Depends(get_db)):
    db_shop = crud_shop.update_shop(db, shop_id=shop_id, shop=shop)
    if db_shop is None:
        raise HTTPException(status_code=404, detail="Shop not found")
    return db_shop

@router.delete("/{shop_id}", response_model=ShopBase)
def delete_shop(shop_id: int, db: Session = Depends(get_db)):
    db_shop = crud_shop.delete_shop(db, shop_id=shop_id)
    if db_shop is None:
        raise HTTPException(status_code=404, detail="Shop not found")
    return db_shop