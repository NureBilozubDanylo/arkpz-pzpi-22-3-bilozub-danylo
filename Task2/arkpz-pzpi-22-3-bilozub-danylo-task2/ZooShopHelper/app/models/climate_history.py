from sqlalchemy import Column, Integer, Float, DateTime, ForeignKey
from app.database import Base

class ClimateHistory(Base):
    __tablename__ = "ClimateHistory"
    climate_history_id = Column(Integer, primary_key=True, index=True)
    temperature = Column(Float)
    humidity = Column(Float)
    light_intensity = Column(Float)
    record_date = Column(DateTime)
    shop_id = Column(Integer, ForeignKey("Shop.shop_id"))
