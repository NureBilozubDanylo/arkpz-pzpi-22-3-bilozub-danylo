from sqlalchemy.orm import Session
from app.models.climate_settings import ClimateSettings
from app.schemas.climate_settings import ClimateSettingsCreate, ClimateSettingsUpdate

def create_climate_settings(db: Session, climate_settings: ClimateSettingsCreate):
    db_climate_settings = ClimateSettings(**climate_settings.dict())
    db.add(db_climate_settings)
    db.commit()
    db.refresh(db_climate_settings)
    return db_climate_settings

def get_climate_settings(db: Session, setting_id: int):
    return db.query(ClimateSettings).filter(ClimateSettings.setting_id == setting_id).first()

def update_climate_settings(db: Session, setting_id: int, climate_settings: ClimateSettingsUpdate):
    db_climate_settings = db.query(ClimateSettings).filter(ClimateSettings.setting_id == setting_id).first()
    if db_climate_settings:
        for key, value in climate_settings.dict().items():
            setattr(db_climate_settings, key, value)
        db.commit()
        db.refresh(db_climate_settings)
    return db_climate_settings

def delete_climate_settings(db: Session, setting_id: int):
    db_climate_settings = db.query(ClimateSettings).filter(ClimateSettings.setting_id == setting_id).first()
    if db_climate_settings:
        db.delete(db_climate_settings)
        db.commit()
    return db_climate_settings

def get_climate_settings_by_shop_id(db: Session, shop_id: int):
    return db.query(ClimateSettings).filter(ClimateSettings.shop_id == shop_id).first()
