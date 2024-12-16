from sqlalchemy import Column, Integer, Float, DateTime, ForeignKey
from app.database import Base

class ClimateSettings(Base):
    __tablename__ = "ClimateSettings"
    setting_id = Column(Integer, primary_key=True, index=True)
    temperature = Column(Float)
    humidity = Column(Float)
    light_intensity = Column(Float)
    updated_at = Column(DateTime)
    shop_id = Column(Integer, ForeignKey("Shop.shop_id"))
