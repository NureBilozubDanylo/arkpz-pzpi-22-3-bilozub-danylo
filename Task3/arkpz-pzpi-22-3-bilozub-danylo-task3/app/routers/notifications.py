from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.crud import notification as crud_notification
from app.models.user import User
from app.schemas.notification import Notification, NotificationBase, NotificationCreate, NotificationUpdate
from app.dependencies import get_current_user, get_current_admin_user
from typing import List

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=Notification)
def create_notification(notification: NotificationCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_admin_user)):
    return crud_notification.create_notification(db=db, notification=notification)

@router.get("/{notification_id}", response_model=Notification)
def read_notification(notification_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_notification = crud_notification.get_notification(db, notification_id=notification_id)
    if db_notification is None:
        raise HTTPException(status_code=404, detail="Notification not found")
    return db_notification

@router.get("/user/{user_id}", response_model=List[Notification])
def get_notifications_by_user_id(user_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    notifications = crud_notification.get_notifications_by_user_id(db, user_id=user_id)
    if not notifications:
        raise HTTPException(status_code=404, detail="No notifications found for this user")
    return notifications

@router.put("/{notification_id}", response_model=Notification)
def update_notification(notification_id: int, notification: NotificationUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_admin_user)):
    db_notification = crud_notification.update_notification(db, notification_id=notification_id, notification=notification)
    if db_notification is None:
        raise HTTPException(status_code=404, detail="Notification not found")
    return db_notification

@router.delete("/{notification_id}", response_model=Notification)
def delete_notification(notification_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_admin_user)):
    db_notification = crud_notification.delete_notification(db, notification_id=notification_id)
    if db_notification is None:
        raise HTTPException(status_code=404, detail="Notification not found")
    return db_notification