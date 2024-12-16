from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from app.models.animal import Animal
from app.models.climate_settings import ClimateSettings
from app.models.notification import Notification
from app.schemas.animal import AnimalCreate, AnimalUpdate
from app.schemas.climate_settings import ClimateSettingsCreate, ClimateSettingsUpdate
from app.schemas.notification import NotificationCreate
from app.crud import notification as crud_notification
from app.crud import user_in_shop as crud_user_in_shop
import numpy as np

# Create
def create_animal(db: Session, animal: AnimalCreate):
    db_animal = Animal(
        name=animal.name,
        species=animal.species,
        breed=animal.breed,
        age=animal.age,
        sex=animal.sex,
        weight=animal.weight,
        health_info=animal.health_info,
        shop_id=animal.shop_id,
        temperature=animal.temperature,
        humidity=animal.humidity,
        light_intensity=animal.light_intensity,
        feeding_time=animal.feeding_time,
        food_weight=animal.food_weight,
        food_name=animal.food_name
    )
    db.add(db_animal)
    db.commit()
    db.refresh(db_animal)

    update_climate_settings(db, animal.shop_id)

    return db_animal

# Read
def get_animal(db: Session, animal_id: int):
    return db.query(Animal).filter(Animal.animal_id == animal_id).first()

def get_animals_by_shop_id(db: Session, shop_id: int):
    return db.query(Animal).filter(Animal.shop_id == shop_id).all()

# Delete
def delete_animal(db: Session, animal_id: int):
    db_animal = db.query(Animal).filter(Animal.animal_id == animal_id).first()
    if db_animal:
        shop_id = db_animal.shop_id
        db.delete(db_animal)
        db.commit()

        update_climate_settings(db, shop_id)
    
    return db_animal

def update_animal(db: Session, animal_id: int, animal_update: AnimalUpdate):
    db_animal = db.query(Animal).filter(Animal.animal_id == animal_id).first()
    if db_animal:
        for key, value in animal_update.dict(exclude_unset=True).items():
            setattr(db_animal, key, value)
        db.commit()
        db.refresh(db_animal)

    update_climate_settings(db, db_animal.shop_id)
    return db_animal

def update_climate_settings(db: Session, shop_id: int):
    animals = db.query(Animal).filter(Animal.shop_id == shop_id).all()
    if animals:
        temperatures = [a.temperature for a in animals]
        humidities = [a.humidity for a in animals]
        light_intensities = [a.light_intensity for a in animals]
        weights = [a.weight for a in animals]

        # Temperature: Weighted median
        # Calculate the weighted average temperature
        total_weight = sum(a.weight for a in animals)
        if total_weight == 0:
            weighted_median_temperature = 0  # Handle the case with no weight
        else:
            weighted_median_temperature = sum(a.temperature * a.weight for a in animals) / total_weight



        # Optimal humidity
        humidities = [a.humidity for a in animals]
        high_humidity_animals = [a for a in animals if a.humidity > 75]

        if high_humidity_animals:
            high_humidity_values = [a.humidity for a in high_humidity_animals]
            optimal_humidity = np.percentile(high_humidity_values, 75)
        else:
            lower_percentile = np.percentile(humidities, 25)
            upper_percentile = np.percentile(humidities, 75)
            optimal_humidity = (lower_percentile + upper_percentile) / 2

        # Optimal light intensity
        light_intensities = [a.light_intensity for a in animals]
        max_light_intensity = max(light_intensities)
        median_light_intensity = np.median(light_intensities)
        optimal_light_intensity = min(max_light_intensity, median_light_intensity)


        db_climate_settings = db.query(ClimateSettings).filter(ClimateSettings.shop_id == shop_id).first()
        if db_climate_settings:
            db_climate_settings.temperature = weighted_median_temperature
            db_climate_settings.humidity = optimal_humidity
            db_climate_settings.light_intensity = optimal_light_intensity
            db_climate_settings.updated_at = datetime.now()
        else:
            new_climate_settings = ClimateSettingsCreate(
                temperature=weighted_median_temperature,
                humidity=optimal_humidity,
                light_intensity=optimal_light_intensity,
                updated_at=datetime.now(),
                shop_id=shop_id
            )
            db_climate_settings = ClimateSettings(**new_climate_settings.dict())
            db.add(db_climate_settings)
        
        db.commit()
        db.refresh(db_climate_settings)

def check_feeding_times(db: Session):
    now = datetime.now()
    ten_minutes_later = now + timedelta(minutes=10)
    animals = db.query(Animal).all()
    for animal in animals:
        feeding_times = animal.feeding_time.split(',')
        for feeding_time in feeding_times:
            feeding_datetime = datetime.strptime(feeding_time.strip(), "%H:%M").replace(year=now.year, month=now.month, day=now.day)
            if now <= feeding_datetime <= ten_minutes_later:
                message = f"Time to feed {animal.name} ({animal.species}) in shop {animal.shop_id}."
                print(message)
                users_in_shop = crud_user_in_shop.get_users_in_shop_by_shop_id(db, shop_id=animal.shop_id)
                for user_in_shop in users_in_shop:
                    notification = NotificationCreate(
                        user_id=user_in_shop.user_id,
                        message=message,
                        timestamp=now
                    )
                    crud_notification.create_notification(db=db, notification=notification)
