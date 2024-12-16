
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.crud import shop_supplies as crud_shop_supplies
from app.schemas.shop_supplies import ShopSuppliesBase, ShopSuppliesCreate, ShopSuppliesUpdate

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=ShopSuppliesBase)
def create_shop_supplies(shop_supplies: ShopSuppliesCreate, db: Session = Depends(get_db)):
    return crud_shop_supplies.create_shop_supplies(db=db, shop_supplies=shop_supplies)

@router.get("/{shop_supplies_id}", response_model=ShopSuppliesBase)
def read_shop_supplies(shop_supplies_id: int, db: Session = Depends(get_db)):
    db_shop_supplies = crud_shop_supplies.get_shop_supplies(db, shop_supplies_id=shop_supplies_id)
    if db_shop_supplies is None:
        raise HTTPException(status_code=404, detail="Shop supplies not found")
    return db_shop_supplies

@router.put("/{shop_supplies_id}", response_model=ShopSuppliesBase)
def update_shop_supplies(shop_supplies_id: int, shop_supplies: ShopSuppliesUpdate, db: Session = Depends(get_db)):
    db_shop_supplies = crud_shop_supplies.update_shop_supplies(db, shop_supplies_id=shop_supplies_id, shop_supplies=shop_supplies)
    if db_shop_supplies is None:
        raise HTTPException(status_code=404, detail="Shop supplies not found")
    return db_shop_supplies

@router.delete("/{shop_supplies_id}", response_model=ShopSuppliesBase)
def delete_shop_supplies(shop_supplies_id: int, db: Session = Depends(get_db)):
    db_shop_supplies = crud_shop_supplies.delete_shop_supplies(db, shop_supplies_id=shop_supplies_id)
    if db_shop_supplies is None:
        raise HTTPException(status_code=404, detail="Shop supplies not found")
    return db_shop_supplies