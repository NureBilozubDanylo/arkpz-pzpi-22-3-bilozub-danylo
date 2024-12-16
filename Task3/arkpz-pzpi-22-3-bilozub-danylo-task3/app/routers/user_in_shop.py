from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.crud import user_in_shop as crud_user_in_shop
from app.dependencies import get_current_admin_user,get_current_user
from app.models.user import User
from app.schemas.user_in_shop import UserInShop, UserInShopBase, UserInShopCreate, UserInShopUpdate

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=UserInShop)
def create_user_in_shop(user_in_shop: UserInShopCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_admin_user)):
    return crud_user_in_shop.create_user_in_shop(db=db, user_in_shop=user_in_shop)

@router.post("/assign", response_model=UserInShop)
def assign_user_to_shop(user_in_shop: UserInShopCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_admin_user)):
    db_user_in_shop = crud_user_in_shop.create_user_in_shop(db=db, user_in_shop=user_in_shop)
    return db_user_in_shop

@router.get("/{user_in_shop_id}", response_model=UserInShop)
def read_user_in_shop(user_in_shop_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_user_in_shop = crud_user_in_shop.get_user_in_shop(db, user_in_shop_id=user_in_shop_id)
    if db_user_in_shop is None:
        raise HTTPException(status_code=404, detail="User in shop not found")
    return db_user_in_shop

@router.put("/{user_in_shop_id}", response_model=UserInShop)
def update_user_in_shop(user_in_shop_id: int, user_in_shop: UserInShopUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_admin_user)):
    db_user_in_shop = crud_user_in_shop.update_user_in_shop(db, user_in_shop_id=user_in_shop_id, user_in_shop=user_in_shop)
    if db_user_in_shop is None:
        raise HTTPException(status_code=404, detail="User in shop not found")
    return db_user_in_shop

@router.delete("/{user_in_shop_id}", response_model=UserInShop)
def delete_user_in_shop(user_in_shop_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_admin_user)):
    db_user_in_shop = crud_user_in_shop.delete_user_in_shop(db, user_in_shop_id=user_in_shop_id)
    if db_user_in_shop is None:
        raise HTTPException(status_code=404, detail="User in shop not found")
    return db_user_in_shop