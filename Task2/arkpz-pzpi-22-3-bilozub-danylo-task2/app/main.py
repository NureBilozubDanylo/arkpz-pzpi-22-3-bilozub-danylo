from fastapi import FastAPI
from app.database import engine, Base
from app.database import SessionLocal 
from app.crud.user import create_user, get_user
from app.schemas.user import UserCreate
from app.models import user
from app.models import animal
from app.models import climate_history
from app.models import climate_settings
from app.models import shop
from app.models import notification
from app.models import sensor
from app.models import shop_supplies
from app.models import supplies
from app.models import user_in_shop

from app.routers import animal, user, climate_settings, climate_history, notifications, sensor, shop_supplies, shop, user_in_shop, supplies, auth


app = FastAPI()
app.include_router(animal.router, prefix="/animals", tags=["Animals"])
app.include_router(user.router, prefix="/users", tags=["Users"])
app.include_router(climate_settings.router, prefix="/climate_settings", tags=["Climate_settings"])
app.include_router(climate_history.router, prefix="/climate_history", tags=["Climate_history"])
app.include_router(notifications.router, prefix="/notifications", tags=["Notifications"])
app.include_router(sensor.router, prefix="/sensors", tags=["Sensors"])
app.include_router(shop_supplies.router, prefix="/shop_supplies", tags=["Shop_supplies"])
app.include_router(shop.router, prefix="/shops", tags=["Shops"])
app.include_router(user_in_shop.router, prefix="/user_in_shop", tags=["User_in_shop"])
app.include_router(supplies.router, prefix="/supplies", tags=["Supplies"])
app.include_router(auth.router, prefix="/auth", tags=["Auth"])


@app.get("/") 
def read_root(): 
    return {"message": "Welcome to the API"}

Base.metadata.create_all(engine)

new_user_data = UserCreate(
    username="qqdвііwввadaddasвівіdsdsdвівіsadssdsasdsdsddsdssdsdфіывавіаіввясвіівічсввіsadвdsdіdsewsdfввівіdуіваsdsівs1",
    password="testpass",
    role="admin",
    email="test@example.com",
    mobile_number="1234567890",
    age=30
)

db = SessionLocal()
new_user = create_user(db, new_user_data) 
user = get_user(db, user_id=1) 
print(user)
db.close()