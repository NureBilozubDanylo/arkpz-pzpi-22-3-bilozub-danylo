from pydantic import BaseModel

class ShopBase(BaseModel):
    name: str
    location: str
    work_schedule: str
    class Config:
        orm_mode = True

class ShopCreate(ShopBase):
    pass

class ShopUpdate(ShopBase):
    pass

class Shop(ShopBase):
    shop_id: int

    class Config:
        orm_mode = True
