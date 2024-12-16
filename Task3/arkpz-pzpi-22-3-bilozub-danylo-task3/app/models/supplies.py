from sqlalchemy import Column, Integer, String
from app.database import Base

class Supplies(Base):
    __tablename__ = "Supplies"
    supply_id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
