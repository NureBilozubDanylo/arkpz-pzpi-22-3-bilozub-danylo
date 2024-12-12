
from pydantic import BaseModel

class ShopSuppliesBase(BaseModel):
    shop_id: int
    supply_id: int
    quantity: int
    class Config:
        orm_mode = True

class ShopSuppliesCreate(ShopSuppliesBase):
    pass

class ShopSuppliesUpdate(ShopSuppliesBase):
    pass

class ShopSupplies(ShopSuppliesBase):
    shop_supplies_id: int

    class Config:
        orm_mode = True