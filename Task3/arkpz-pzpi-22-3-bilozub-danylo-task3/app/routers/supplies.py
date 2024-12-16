
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.crud import supplies as crud_supplies
from app.models.user import User
from app.schemas.supplies import Supplies, SuppliesBase, SuppliesCreate, SuppliesUpdate
from app.dependencies import get_current_user, get_current_admin_user

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=Supplies)
def create_supplies(supplies: SuppliesCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_admin_user)):
    return crud_supplies.create_supplies(db=db, supplies=supplies)

@router.get("/{supply_id}", response_model=Supplies)
def read_supplies(supply_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_supplies = crud_supplies.get_supplies(db, supply_id=supply_id)
    if db_supplies is None:
        raise HTTPException(status_code=404, detail="Supplies not found")
    return db_supplies

@router.put("/{supply_id}", response_model=Supplies)
def update_supplies(supply_id: int, supplies: SuppliesUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_admin_user)):
    db_supplies = crud_supplies.update_supplies(db, supply_id=supply_id, supplies=supplies)
    if db_supplies is None:
        raise HTTPException(status_code=404, detail="Supplies not found")
    return db_supplies

@router.delete("/{supply_id}", response_model=Supplies)
def delete_supplies(supply_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_admin_user)):
    db_supplies = crud_supplies.delete_supplies(db, supply_id=supply_id)
    if db_supplies is None:
        raise HTTPException(status_code=404, detail="Supplies not found")
    return db_supplies