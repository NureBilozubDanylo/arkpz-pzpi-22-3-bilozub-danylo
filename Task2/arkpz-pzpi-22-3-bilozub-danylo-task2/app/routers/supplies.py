
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.crud import supplies as crud_supplies
from app.schemas.supplies import SuppliesBase, SuppliesCreate, SuppliesUpdate

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=SuppliesBase)
def create_supplies(supplies: SuppliesCreate, db: Session = Depends(get_db)):
    return crud_supplies.create_supplies(db=db, supplies=supplies)

@router.get("/{supplies_id}", response_model=SuppliesBase)
def read_supplies(supplies_id: int, db: Session = Depends(get_db)):
    db_supplies = crud_supplies.get_supplies(db, supplies_id=supplies_id)
    if db_supplies is None:
        raise HTTPException(status_code=404, detail="Supplies not found")
    return db_supplies

@router.put("/{supplies_id}", response_model=SuppliesBase)
def update_supplies(supplies_id: int, supplies: SuppliesUpdate, db: Session = Depends(get_db)):
    db_supplies = crud_supplies.update_supplies(db, supplies_id=supplies_id, supplies=supplies)
    if db_supplies is None:
        raise HTTPException(status_code=404, detail="Supplies not found")
    return db_supplies

@router.delete("/{supplies_id}", response_model=SuppliesBase)
def delete_supplies(supplies_id: int, db: Session = Depends(get_db)):
    db_supplies = crud_supplies.delete_supplies(db, supplies_id=supplies_id)
    if db_supplies is None:
        raise HTTPException(status_code=404, detail="Supplies not found")
    return db_supplies