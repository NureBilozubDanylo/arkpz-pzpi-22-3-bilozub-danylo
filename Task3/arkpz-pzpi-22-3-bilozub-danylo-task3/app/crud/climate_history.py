from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import date, datetime
from app.models.climate_history import ClimateHistory
from app.schemas.climate_history import ClimateHistoryCreate, ClimateHistoryUpdate, ClimateHistoryBase

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

def get_daily_climate_history(db: Session, shop_id: int, date: date):
    return db.query(ClimateHistory).filter(
        ClimateHistory.shop_id == shop_id,
        func.date(ClimateHistory.record_date) == date
    ).all()

def get_monthly_climate_history(db: Session, shop_id: int, month: int, year: int):
    return db.query(ClimateHistory).filter(
        ClimateHistory.shop_id == shop_id,
        func.extract('month', ClimateHistory.record_date) == month,
        func.extract('year', ClimateHistory.record_date) == year
    ).all()

def get_average_climate_history(db: Session, shop_id: int):
    avg_values = db.query(
        func.avg(ClimateHistory.temperature).label('temperature'),
        func.avg(ClimateHistory.humidity).label('humidity'),
        func.avg(ClimateHistory.light_intensity).label('light_intensity')
    ).filter(ClimateHistory.shop_id == shop_id).first()
    
    return ClimateHistoryBase(
        temperature=avg_values.temperature,
        humidity=avg_values.humidity,
        light_intensity=avg_values.light_intensity,
        record_date=datetime.utcnow(),
        shop_id=shop_id
    )

def get_mode_climate_history(db: Session, shop_id: int):
    from sqlalchemy import func
    from collections import Counter

    def get_mode(values):
        if not values:
            return None
        counter = Counter(values)
        mode, _ = counter.most_common(1)[0]
        return mode

    temperatures = db.query(ClimateHistory.temperature).filter(ClimateHistory.shop_id == shop_id).all()
    humidities = db.query(ClimateHistory.humidity).filter(ClimateHistory.shop_id == shop_id).all()
    light_intensities = db.query(ClimateHistory.light_intensity).filter(ClimateHistory.shop_id == shop_id).all()

    mode_temperature = get_mode([t[0] for t in temperatures])
    mode_humidity = get_mode([h[0] for h in humidities])
    mode_light_intensity = get_mode([l[0] for l in light_intensities])

    return ClimateHistoryBase(
        temperature=mode_temperature,
        humidity=mode_humidity,
        light_intensity=mode_light_intensity,
        record_date=datetime.utcnow(),
        shop_id=shop_id
    )
