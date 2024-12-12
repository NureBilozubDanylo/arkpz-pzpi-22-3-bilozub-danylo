from sqlalchemy import Column, Integer, String
from app.database import Base

class Shop(Base):
    __tablename__ = "Shop"
    shop_id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    location = Column(String)
    work_schedule = Column(String)
