from datetime import datetime
from sqlalchemy.orm import Session
from app.models.animal import Animal
from app.models.climate_settings import ClimateSettings
from app.schemas.animal import AnimalCreate, AnimalUpdate
from app.schemas.climate_settings import ClimateSettingsCreate, ClimateSettingsUpdate

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
        avg_temperature = sum(a.temperature for a in animals) / len(animals)
        avg_humidity = sum(a.humidity for a in animals) / len(animals)
        avg_light_intensity = sum(a.light_intensity for a in animals) / len(animals)

        db_climate_settings = db.query(ClimateSettings).filter(ClimateSettings.shop_id == shop_id).first()
        if db_climate_settings:
            db_climate_settings.temperature = avg_temperature
            db_climate_settings.humidity = avg_humidity
            db_climate_settings.light_intensity = avg_light_intensity
            db_climate_settings.updated_at = datetime.utcnow()
        else:
            new_climate_settings = ClimateSettingsCreate(
                temperature=avg_temperature,
                humidity=avg_humidity,
                light_intensity=avg_light_intensity,
                updated_at=datetime.utcnow(),
                shop_id=shop_id
            )
            db_climate_settings = ClimateSettings(**new_climate_settings.dict())
            db.add(db_climate_settings)
        
        db.commit()
        db.refresh(db_climate_settings)
