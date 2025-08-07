from sqlalchemy import Column, Integer, String
from .base import Base

class Item(Base):
    __tablename__ = 'items'
    id = Column(Integer, primary_key=True)
    item_id = Column(String, unique=True)
    name = Column(String)
    item_type = Column(String)
    rarity = Column(String)
    description = Column(String)
