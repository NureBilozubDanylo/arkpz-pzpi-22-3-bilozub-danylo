from pydantic import BaseModel, Field, validator
from datetime import datetime

class AnimalBase(BaseModel):
    animal_id: int
    name: str
    species: str
    breed: str
    age: int
    sex: str
    weight: float
    health_info: str
    shop_id: int
    temperature: float = Field(..., ge=0, le=50, description="Temperature must be between 0 and 50 degrees Celsius")
    humidity: float = Field(..., ge=0, le=100, description="Humidity must be between 0 and 100 percent")
    light_intensity: float = Field(..., ge=0, le=100000, description="Light intensity must be between 0 and 100000 lux")
    feeding_time: str
    food_weight: float
    food_name: str
    class Config:
        orm_mode = True

class AnimalCreate(BaseModel):
    name: str
    species: str
    breed: str
    age: int
    sex: str
    weight: float
    health_info: str
    shop_id: int
    temperature: float = Field(..., ge=0, le=50, description="Temperature must be between 0 and 50 degrees Celsius")
    humidity: float = Field(..., ge=0, le=100, description="Humidity must be between 0 and 100 percent")
    light_intensity: float = Field(..., ge=0, le=100000, description="Light intensity must be between 0 and 100000 lux")
    feeding_time: str
    food_weight: float
    food_name: str
    class Config:
        orm_mode = True

class AnimalUpdate(BaseModel):
    name: str
    species: str
    breed: str
    age: int
    sex: str
    weight: float
    health_info: str
    shop_id: int
    temperature: float = Field(..., ge=0, le=50, description="Temperature must be between 0 and 50 degrees Celsius")
    humidity: float = Field(..., ge=0, le=100, description="Humidity must be between 0 and 100 percent")
    light_intensity: float = Field(..., ge=0, le=100000, description="Light intensity must be between 0 and 100000 lux")
    feeding_time: str
    food_weight: float
    food_name: str
    class Config:
        orm_mode = True