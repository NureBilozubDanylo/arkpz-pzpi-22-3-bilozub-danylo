from sqlalchemy import Column, Integer, String, DateTime, Float, Text, ForeignKey, JSON
from app.database import Base

class Animal(Base):
    __tablename__ = "Animal"
    animal_id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    species = Column(String)
    breed = Column(String)
    age = Column(Integer)
    sex = Column(String)
    weight = Column(Float)
    health_info = Column(Text)
    shop_id = Column(Integer, ForeignKey("Shop.shop_id"))
    temperature = Column(Float)
    humidity = Column(Float)
    light_intensity = Column(Float)
    feeding_time = Column(String)
    food_weight = Column(Float)
    food_name = Column(String)
