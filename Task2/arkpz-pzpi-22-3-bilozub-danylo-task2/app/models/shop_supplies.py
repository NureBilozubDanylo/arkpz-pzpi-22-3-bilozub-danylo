from sqlalchemy import Column, Integer, ForeignKey
from app.database import Base

class ShopSupplies(Base):
    __tablename__ = "ShopSupplies"
    shop_supplies_id = Column(Integer, primary_key=True, index=True)
    shop_id = Column(Integer, ForeignKey("Shop.shop_id"))
    supply_id = Column(Integer, ForeignKey("Supplies.supply_id"))
    quantity = Column(Integer)
