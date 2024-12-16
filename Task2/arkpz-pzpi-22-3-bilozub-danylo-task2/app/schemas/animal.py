from pydantic import BaseModel
from datetime import datetime

class AnimalBase(BaseModel):
    name: str
    species: str
    breed: str
    age: int
    sex: str
    weight: float
    health_info: str
    shop_id: int
    temperature: float
    humidity: float
    light_intensity: float
    feeding_time: str
    food_weight: float
    food_name: str
    class Config:
        orm_mode = True

class AnimalCreate(AnimalBase):
    pass

class AnimalUpdate(AnimalBase):
    pass