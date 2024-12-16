from sqlalchemy.orm import Session
from app.models.sensor import Sensor
from app.schemas.sensor import SensorCreate, SensorUpdate

def create_sensor(db: Session, sensor: SensorCreate):
    db_sensor = Sensor(**sensor.dict())
    db.add(db_sensor)
    db.commit()
    db.refresh(db_sensor)
    return db_sensor

def get_sensor(db: Session, sensor_id: int):
    return db.query(Sensor).filter(Sensor.sensor_id == sensor_id).first()

def update_sensor(db: Session, sensor_id: int, sensor: SensorUpdate):
    db_sensor = db.query(Sensor).filter(Sensor.sensor_id == sensor_id).first()
    if db_sensor:
        for key, value in sensor.dict().items():
            setattr(db_sensor, key, value)
        db.commit()
        db.refresh(db_sensor)
    return db_sensor

def delete_sensor(db: Session, sensor_id: int):
    db_sensor = db.query(Sensor).filter(Sensor.sensor_id == sensor_id).first()
    if db_sensor:
        db.delete(db_sensor)
        db.commit()
    return db_sensor

def get_sensors_by_shop_id(db: Session, shop_id: int):
    return db.query(Sensor).filter(Sensor.shop_id == shop_id).all()
