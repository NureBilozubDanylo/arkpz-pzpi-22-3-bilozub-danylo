from datetime import datetime
from pydantic import BaseModel

class SensorBase(BaseModel):
    type: str
    location: str
    current_value: float
    last_maintenance: datetime
    shop_id: int
    sensor_link: str
    class Config:
        orm_mode = True

class SensorCreate(SensorBase):
    pass

class SensorUpdate(SensorBase):
    pass

class Sensor1(SensorBase):
    sensor_id: int

    class Config:
        orm_mode = True
