from sqlalchemy import Column, Integer, String
from app.database import Base

class User(Base):
    __tablename__ = "Users"
    user_id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    password = Column(String)
    role = Column(String)
    email = Column(String)
    mobile_number = Column(String)
    age = Column(Integer)
