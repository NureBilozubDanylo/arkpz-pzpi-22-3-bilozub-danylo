from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class ClimateHistoryBase(BaseModel):
    temperature: float
    humidity: Optional[float]
    light_intensity: Optional[float]
    record_date: datetime
    shop_id: int

class ClimateHistoryCreate(ClimateHistoryBase):
    pass

class ClimateHistoryUpdate(ClimateHistoryBase):
    pass

class ClimateHistory(ClimateHistoryBase):
    climate_history_id: int

    class Config:
        orm_mode = True
