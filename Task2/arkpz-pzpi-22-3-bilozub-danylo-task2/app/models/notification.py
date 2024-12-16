from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from app.database import Base

class Notification(Base):
    __tablename__ = "Notification"
    notification_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("Users.user_id"))
    message = Column(String)
    timestamp = Column(DateTime)
