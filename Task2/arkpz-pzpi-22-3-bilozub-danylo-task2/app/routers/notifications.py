from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.crud import notification as crud_notification
from app.schemas.notification import NotificationBase, NotificationCreate, NotificationUpdate

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=NotificationBase)
def create_notification(notification: NotificationCreate, db: Session = Depends(get_db)):
    return crud_notification.create_notification(db=db, notification=notification)

@router.get("/{notification_id}", response_model=NotificationBase)
def read_notification(notification_id: int, db: Session = Depends(get_db)):
    db_notification = crud_notification.get_notification(db, notification_id=notification_id)
    if db_notification is None:
        raise HTTPException(status_code=404, detail="Notification not found")
    return db_notification

@router.put("/{notification_id}", response_model=NotificationBase)
def update_notification(notification_id: int, notification: NotificationUpdate, db: Session = Depends(get_db)):
    db_notification = crud_notification.update_notification(db, notification_id=notification_id, notification=notification)
    if db_notification is None:
        raise HTTPException(status_code=404, detail="Notification not found")
    return db_notification

@router.delete("/{notification_id}", response_model=NotificationBase)
def delete_notification(notification_id: int, db: Session = Depends(get_db)):
    db_notification = crud_notification.delete_notification(db, notification_id=notification_id)
    if db_notification is None:
        raise HTTPException(status_code=404, detail="Notification not found")
    return db_notification