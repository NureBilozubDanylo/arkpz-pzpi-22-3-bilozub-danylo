from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.crud import sensor as crud_sensor
from app.models.climate_settings import ClimateSettings
from app.models.sensor import Sensor
from app.schemas.sensor import Sensor1,SensorBase, SensorCreate, SensorUpdate
from app.models.user import User
from app.dependencies import get_current_user, get_current_admin_user
from app.crud import climate_history as crud_climate_history
from app.schemas.climate_history import ClimateHistoryCreate
from app.crud import notification as crud_notification
from app.schemas.notification import NotificationCreate
from app.crud import user_in_shop as crud_user_in_shop
from typing import List

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=Sensor1)
def create_sensor(sensor: SensorCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_admin_user)):
    return crud_sensor.create_sensor(db=db, sensor=sensor)

@router.get("/{sensor_id}", response_model=Sensor1)
def read_sensor(sensor_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_sensor = crud_sensor.get_sensor(db, sensor_id=sensor_id)
    if db_sensor is None:
        raise HTTPException(status_code=404, detail="Sensor not found")
    return db_sensor

@router.put("/{sensor_id}", response_model=Sensor1)
def update_sensor(sensor_id: int, sensor: SensorUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_admin_user)):
    db_sensor = crud_sensor.update_sensor(db, sensor_id=sensor_id, sensor=sensor)
    if db_sensor is None:
        raise HTTPException(status_code=404, detail="Sensor not found")
    return db_sensor

@router.put("/{sensor_id}/value", response_model=Sensor1)
def update_sensor_value(sensor_id: int, value: float, db: Session = Depends(get_db), current_user: User = Depends(get_current_admin_user)):
    db_sensor = crud_sensor.get_sensor(db, sensor_id=sensor_id)
    if db_sensor is None:
        raise HTTPException(status_code=404, detail="Sensor not found")
    
    db_sensor.current_value = value
    db.commit()
    db.refresh(db_sensor)
    
    db_climate_settings = db.query(ClimateSettings).filter(ClimateSettings.shop_id == db_sensor.shop_id).first()
    if db_climate_settings:
        warning_message = None
        if db_sensor.type == "temperature" and abs(db_sensor.current_value - db_climate_settings.temperature) > 3:
            warning_message = f"Warning: Sensor value {db_sensor.current_value} deviates from climate setting temperature {db_climate_settings.temperature} by more than 10%."
        elif db_sensor.type == "humidity" and abs(db_sensor.current_value - db_climate_settings.humidity) > 3:
            warning_message = f"Warning: Sensor value {db_sensor.current_value} deviates from climate setting humidity {db_climate_settings.humidity} by more than 10%."
        elif db_sensor.type == "light_intensity" and abs(db_sensor.current_value - db_climate_settings.light_intensity) > 3:
            warning_message = f"Warning: Sensor value {db_sensor.current_value} deviates from climate setting light intensity {db_climate_settings.light_intensity} by more than 10%."
        
        if warning_message:
            print(warning_message)
            users_in_shop = crud_user_in_shop.get_users_in_shop_by_shop_id(db, shop_id=db_sensor.shop_id)
            for user_in_shop in users_in_shop:
                notification = NotificationCreate(
                    user_id=user_in_shop.user_id,
                    message=warning_message,
                    timestamp=datetime.now()
                )
                crud_notification.create_notification(db=db, notification=notification)
    
    sensors = db.query(Sensor).filter(Sensor.shop_id == db_sensor.shop_id).all()
    temperature = humidity = light_intensity = None
    for sensor in sensors:
        if sensor.type == "temperature":
            temperature = sensor.current_value
        elif sensor.type == "humidity":
            humidity = sensor.current_value
        elif sensor.type == "light_intensity":
            light_intensity = sensor.current_value
    
    climate_history = ClimateHistoryCreate(
        temperature=temperature,
        humidity=humidity,
        light_intensity=light_intensity,
        record_date=datetime.now(),
        shop_id=db_sensor.shop_id
    )
    crud_climate_history.create_climate_history(db=db, climate_history=climate_history)
    
    return db_sensor

@router.delete("/{sensor_id}", response_model=Sensor1)
def delete_sensor(sensor_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_admin_user)):
    db_sensor = crud_sensor.delete_sensor(db, sensor_id=sensor_id)
    if db_sensor is None:
        raise HTTPException(status_code=404, detail="Sensor not found")
    return db_sensor

@router.get("/shop/{shop_id}/sensors", response_model=List[Sensor1])
def get_sensors_by_shop_id(shop_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    sensors = crud_sensor.get_sensors_by_shop_id(db, shop_id=shop_id)
    if not sensors:
        raise HTTPException(status_code=404, detail="No sensors found for this shop")
    return sensors