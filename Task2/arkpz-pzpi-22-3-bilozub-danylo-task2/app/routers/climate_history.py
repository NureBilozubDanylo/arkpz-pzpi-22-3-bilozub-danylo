from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.crud import climate_history as crud_climate_history
from app.schemas.climate_history import ClimateHistoryBase, ClimateHistoryCreate, ClimateHistoryUpdate

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=ClimateHistoryBase)
def create_climate_history(climate_history: ClimateHistoryCreate, db: Session = Depends(get_db)):
    return crud_climate_history.create_climate_history(db=db, climate_history=climate_history)

@router.get("/{climate_history_id}", response_model=ClimateHistoryBase)
def read_climate_history(climate_history_id: int, db: Session = Depends(get_db)):
    db_climate_history = crud_climate_history.get_climate_history(db, climate_history_id=climate_history_id)
    if db_climate_history is None:
        raise HTTPException(status_code=404, detail="Climate history not found")
    return db_climate_history

@router.put("/{climate_history_id}", response_model=ClimateHistoryBase)
def update_climate_history(climate_history_id: int, climate_history: ClimateHistoryUpdate, db: Session = Depends(get_db)):
    db_climate_history = crud_climate_history.update_climate_history(db, climate_history_id=climate_history_id, climate_history=climate_history)
    if db_climate_history is None:
        raise HTTPException(status_code=404, detail="Climate history not found")
    return db_climate_history

@router.delete("/{climate_history_id}", response_model=ClimateHistoryBase)
def delete_climate_history(climate_history_id: int, db: Session = Depends(get_db)):
    db_climate_history = crud_climate_history.delete_climate_history(db, climate_history_id=climate_history_id)
    if db_climate_history is None:
        raise HTTPException(status_code=404, detail="Climate history not found")
    return db_climate_history
