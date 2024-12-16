from sqlalchemy.orm import Session
from app.models.notification import Notification
from app.schemas.notification import NotificationCreate, NotificationUpdate

def create_notification(db: Session, notification: NotificationCreate):
    db_notification = Notification(**notification.dict())
    db.add(db_notification)
    db.commit()
    db.refresh(db_notification)
    return db_notification

def get_notification(db: Session, notification_id: int):
    return db.query(Notification).filter(Notification.notification_id == notification_id).first()

def get_notifications(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Notification).offset(skip).limit(limit).all()

def get_notifications_by_user_id(db: Session, user_id: int):
    return db.query(Notification).filter(Notification.user_id == user_id).all()

def update_notification(db: Session, notification_id: int, notification: NotificationUpdate):
    db_notification = db.query(Notification).filter(Notification.notification_id == notification_id).first()
    if db_notification:
        for key, value in notification.dict().items():
            setattr(db_notification, key, value)
        db.commit()
        db.refresh(db_notification)
    return db_notification

def delete_notification(db: Session, notification_id: int):
    db_notification = db.query(Notification).filter(Notification.notification_id == notification_id).first()
    if db_notification:
        db.delete(db_notification)
        db.commit()
    return db_notification