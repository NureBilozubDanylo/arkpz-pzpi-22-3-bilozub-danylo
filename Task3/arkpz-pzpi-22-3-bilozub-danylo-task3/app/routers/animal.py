from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.crud import animal as crud_animal
from app.schemas.animal import AnimalBase, AnimalCreate, AnimalUpdate
from app.crud.user import get_user, get_user_by_username
from app.schemas.user import UserBase
from app.models.user import User
from app.dependencies import get_current_user, get_current_admin_user
from typing import List

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=AnimalBase)
def create_animal(animal: AnimalCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_admin_user)):
    return crud_animal.create_animal(db=db, animal=animal)

@router.get("/{animal_id}", response_model=AnimalBase)
def read_animal(animal_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_animal = crud_animal.get_animal(db, animal_id=animal_id)
    if db_animal is None:
        raise HTTPException(status_code=404, detail="Animal not found")
    return db_animal

@router.delete("/{animal_id}", response_model=AnimalBase)
def delete_animal(animal_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_admin_user)):
    db_animal = crud_animal.delete_animal(db, animal_id=animal_id)
    if db_animal is None:
        raise HTTPException(status_code=404, detail="Animal not found")
    return db_animal

@router.put("/{animal_id}", response_model=AnimalBase)
def update_animal(animal_id: int, animal: AnimalUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_admin_user)):
    db_animal = crud_animal.update_animal(db, animal_id=animal_id, animal_update=animal)
    if db_animal is None:
        raise HTTPException(status_code=404, detail="Animal not found")
    return db_animal

@router.get("/shop/{shop_id}/animals", response_model=List[AnimalBase])
def get_animals_by_shop_id(shop_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    animals = crud_animal.get_animals_by_shop_id(db, shop_id=shop_id)
    if not animals:
        raise HTTPException(status_code=404, detail="No animals found for this shop")
    return animals