
from pydantic import BaseModel

class SuppliesBase(BaseModel):
    name: str
    
    class Config:
        orm_mode = True

class SuppliesCreate(SuppliesBase):
    pass

class SuppliesUpdate(SuppliesBase):
    pass

class Supplies(SuppliesBase):
    supply_id: int

    class Config:
        orm_mode = True