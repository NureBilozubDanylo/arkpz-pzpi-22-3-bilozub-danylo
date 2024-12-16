from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.crud import climate_settings as crud_climate_settings
from app.schemas.climate_settings import ClimateSettingsBase, ClimateSettingsCreate, ClimateSettingsUpdate

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=ClimateSettingsBase)
def create_climate_settings(climate_settings: ClimateSettingsCreate, db: Session = Depends(get_db)):
    return crud_climate_settings.create_climate_settings(db=db, climate_settings=climate_settings)

@router.get("/{setting_id}", response_model=ClimateSettingsBase)
def read_climate_settings(setting_id: int, db: Session = Depends(get_db)):
    db_climate_settings = crud_climate_settings.get_climate_settings(db, setting_id=setting_id)
    if db_climate_settings is None:
        raise HTTPException(status_code=404, detail="Climate settings not found")
    return db_climate_settings

@router.put("/{setting_id}", response_model=ClimateSettingsBase)
def update_climate_settings(setting_id: int, climate_settings: ClimateSettingsUpdate, db: Session = Depends(get_db)):
    db_climate_settings = crud_climate_settings.update_climate_settings(db, setting_id=setting_id, climate_settings=climate_settings)
    if db_climate_settings is None:
        raise HTTPException(status_code=404, detail="Climate settings not found")
    return db_climate_settings

@router.delete("/{setting_id}", response_model=ClimateSettingsBase)
def delete_climate_settings(setting_id: int, db: Session = Depends(get_db)):
    db_climate_settings = crud_climate_settings.delete_climate_settings(db, setting_id=setting_id)
    if db_climate_settings is None:
        raise HTTPException(status_code=404, detail="Climate settings not found")
    return db_climate_settings
