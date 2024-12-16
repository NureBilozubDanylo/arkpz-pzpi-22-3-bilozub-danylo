from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from app.database import Base

class Sensor(Base):
    __tablename__ = "Sensor"
    sensor_id = Column(Integer, primary_key=True, index=True)
    type = Column(String)
    sensor_link = Column(String)
    location = Column(String)
    current_value = Column(Float)
    last_maintenance = Column(DateTime)
    shop_id = Column(Integer, ForeignKey("Shop.shop_id"))
