from pydantic import BaseModel
from datetime import datetime

class ClimateSettingsBase(BaseModel):
    temperature: float
    humidity: float
    light_intensity: float
    updated_at: datetime
    shop_id: int

class ClimateSettingsCreate(ClimateSettingsBase):
    pass

class ClimateSettingsUpdate(ClimateSettingsBase):
    pass

class ClimateSettings(ClimateSettingsBase):
    setting_id: int

    class Config:
        orm_mode = True
