from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.crud import climate_settings as crud_climate_settings
from app.models.user import User
from app.schemas.climate_settings import ClimateSettings, ClimateSettingsBase, ClimateSettingsCreate, ClimateSettingsUpdate
from app.dependencies import get_current_user, get_current_admin_user
from typing import List

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=ClimateSettings)
def create_climate_settings(climate_settings: ClimateSettingsCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_admin_user)):
    return crud_climate_settings.create_climate_settings(db=db, climate_settings=climate_settings)

@router.get("/{setting_id}", response_model=ClimateSettings)
def read_climate_settings(setting_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_climate_settings = crud_climate_settings.get_climate_settings(db, setting_id=setting_id)
    if db_climate_settings is None:
        raise HTTPException(status_code=404, detail="Climate settings not found")
    return db_climate_settings

@router.put("/{setting_id}", response_model=ClimateSettings)
def update_climate_settings(setting_id: int, climate_settings: ClimateSettingsUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_admin_user)):
    db_climate_settings = crud_climate_settings.update_climate_settings(db, setting_id=setting_id, climate_settings=climate_settings)
    if db_climate_settings is None:
        raise HTTPException(status_code=404, detail="Climate settings not found")
    return db_climate_settings

@router.delete("/{setting_id}", response_model=ClimateSettings)
def delete_climate_settings(setting_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_admin_user)):
    db_climate_settings = crud_climate_settings.delete_climate_settings(db, setting_id=setting_id)
    if db_climate_settings is None:
        raise HTTPException(status_code=404, detail="Climate settings not found")
    return db_climate_settings

@router.get("/shop/{shop_id}", response_model=ClimateSettings)
def get_climate_settings_by_shop_id(shop_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    climate_settings = crud_climate_settings.get_climate_settings_by_shop_id(db, shop_id=shop_id)
    if climate_settings is None:
        raise HTTPException(status_code=404, detail="Climate settings not found for this shop")
    return climate_settings
