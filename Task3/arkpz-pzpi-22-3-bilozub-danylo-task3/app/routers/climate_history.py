from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.crud import climate_history as crud_climate_history
from app.models.user import User
from app.schemas.climate_history import ClimateHistory, ClimateHistoryBase, ClimateHistoryCreate, ClimateHistoryUpdate
from typing import List
from datetime import date, datetime
from app.dependencies import get_current_user, get_current_admin_user

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=ClimateHistory)
def create_climate_history(climate_history: ClimateHistoryCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_admin_user)):
    return crud_climate_history.create_climate_history(db=db, climate_history=climate_history)

@router.get("/{climate_history_id}", response_model=ClimateHistory)
def read_climate_history(climate_history_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_climate_history = crud_climate_history.get_climate_history(db, climate_history_id=climate_history_id)
    if db_climate_history is None:
        raise HTTPException(status_code=404, detail="Climate history not found")
    return db_climate_history

@router.put("/{climate_history_id}", response_model=ClimateHistory)
def update_climate_history(climate_history_id: int, climate_history: ClimateHistoryUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_admin_user)):
    db_climate_history = crud_climate_history.update_climate_history(db, climate_history_id=climate_history_id, climate_history=climate_history)
    if db_climate_history is None:
        raise HTTPException(status_code=404, detail="Climate history not found")
    return db_climate_history

@router.delete("/{climate_history_id}", response_model=ClimateHistory)
def delete_climate_history(climate_history_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_admin_user)):
    db_climate_history = crud_climate_history.delete_climate_history(db, climate_history_id=climate_history_id)
    if db_climate_history is None:
        raise HTTPException(status_code=404, detail="Climate history not found")
    return db_climate_history

@router.get("/shop/{shop_id}/daily", response_model=List[ClimateHistory])
def get_daily_climate_history(shop_id: int, date: date, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return crud_climate_history.get_daily_climate_history(db, shop_id=shop_id, date=date)

@router.get("/shop/{shop_id}/monthly", response_model=List[ClimateHistory])
def get_monthly_climate_history(shop_id: int, month: int, year: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return crud_climate_history.get_monthly_climate_history(db, shop_id=shop_id, month=month, year=year)

@router.get("/shop/{shop_id}/average", response_model=ClimateHistoryBase)
def get_average_climate_history(shop_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return crud_climate_history.get_average_climate_history(db, shop_id=shop_id)

@router.get("/shop/{shop_id}/mode", response_model=ClimateHistoryBase)
def get_mode_climate_history(shop_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return crud_climate_history.get_mode_climate_history(db, shop_id=shop_id)
