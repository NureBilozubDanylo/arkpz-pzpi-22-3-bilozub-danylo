from sqlalchemy.orm import Session
from app.models.climate_history import ClimateHistory
from app.schemas.climate_history import ClimateHistoryCreate, ClimateHistoryUpdate

def create_climate_history(db: Session, climate_history: ClimateHistoryCreate):
    db_climate_history = ClimateHistory(**climate_history.dict())
    db.add(db_climate_history)
    db.commit()
    db.refresh(db_climate_history)
    return db_climate_history

def get_climate_history(db: Session, climate_history_id: int):
    return db.query(ClimateHistory).filter(ClimateHistory.climate_history_id == climate_history_id).first()

def get_climate_history_list(db: Session, skip: int = 0, limit: int = 100):
    return db.query(ClimateHistory).offset(skip).limit(limit).all()

def update_climate_history(db: Session, climate_history_id: int, climate_history: ClimateHistoryUpdate):
    db_climate_history = db.query(ClimateHistory).filter(ClimateHistory.climate_history_id == climate_history_id).first()
    if db_climate_history:
        for key, value in climate_history.dict().items():
            setattr(db_climate_history, key, value)
        db.commit()
        db.refresh(db_climate_history)
    return db_climate_history

def delete_climate_history(db: Session, climate_history_id: int):
    db_climate_history = db.query(ClimateHistory).filter(ClimateHistory.climate_history_id == climate_history_id).first()
    if db_climate_history:
        db.delete(db_climate_history)
        db.commit()
    return db_climate_history
