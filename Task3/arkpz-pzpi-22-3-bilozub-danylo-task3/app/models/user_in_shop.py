from sqlalchemy import Column, Integer, ForeignKey
from app.database import Base

class UserInShop(Base):
    __tablename__ = "UserInShop"
    user_in_shop_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("Users.user_id"))
    shop_id = Column(Integer, ForeignKey("Shop.shop_id"))
