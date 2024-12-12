from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.crud import sensor as crud_sensor
from app.models.climate_settings import ClimateSettings
from app.schemas.sensor import SensorBase, SensorCreate, SensorUpdate
from app.models.user import User
from app.dependencies import get_current_user, get_current_admin_user

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=SensorBase)
def create_sensor(sensor: SensorCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_admin_user)):
    return crud_sensor.create_sensor(db=db, sensor=sensor)

@router.get("/{sensor_id}", response_model=SensorBase)
def read_sensor(sensor_id: int, db: Session = Depends(get_db)):
    db_sensor = crud_sensor.get_sensor(db, sensor_id=sensor_id)
    if db_sensor is None:
        raise HTTPException(status_code=404, detail="Sensor not found")
    return db_sensor

@router.put("/{sensor_id}", response_model=SensorBase)
def update_sensor(sensor_id: int, sensor: SensorUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_admin_user)):
    db_sensor = crud_sensor.update_sensor(db, sensor_id=sensor_id, sensor=sensor)
    if db_sensor is None:
        raise HTTPException(status_code=404, detail="Sensor not found")
    return db_sensor

@router.put("/{sensor_id}/value", response_model=SensorBase)
def update_sensor_value(sensor_id: int, value: float, db: Session = Depends(get_db)):
    db_sensor = crud_sensor.get_sensor(db, sensor_id=sensor_id)
    if db_sensor is None:
        raise HTTPException(status_code=404, detail="Sensor not found")
    
    db_sensor.current_value = value
    db.commit()
    db.refresh(db_sensor)
    
    db_climate_settings = db.query(ClimateSettings).filter(ClimateSettings.shop_id == db_sensor.shop_id).first()
    if db_climate_settings:
        if db_sensor.type == "temperature" and abs(db_sensor.current_value - db_climate_settings.temperature) > 3:
            print(f"Warning: Sensor value {db_sensor.current_value} deviates from climate setting temperature {db_climate_settings.temperature} by more than 3 units.")
        elif db_sensor.type == "humidity" and abs(db_sensor.current_value - db_climate_settings.humidity) > 3:
            print(f"Warning: Sensor value {db_sensor.current_value} deviates from climate setting humidity {db_climate_settings.humidity} by more than 3 units.")
        elif db_sensor.type == "light_intensity" and abs(db_sensor.current_value - db_climate_settings.light_intensity) > 3:
            print(f"Warning: Sensor value {db_sensor.current_value} deviates from climate setting light intensity {db_climate_settings.light_intensity} by more than 3 units.")
    
    return db_sensor

@router.delete("/{sensor_id}", response_model=SensorBase)
def delete_sensor(sensor_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_admin_user)):
    db_sensor = crud_sensor.delete_sensor(db, sensor_id=sensor_id)
    if db_sensor is None:
        raise HTTPException(status_code=404, detail="Sensor not found")
    return db_sensor