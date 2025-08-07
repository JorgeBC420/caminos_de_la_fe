from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base

class Inventory(Base):
    __tablename__ = 'inventories'
    id = Column(Integer, primary_key=True)
    player_id = Column(Integer, ForeignKey('players.id'))
    items = relationship('InventoryItem', back_populates='inventory')

class InventoryItem(Base):
    __tablename__ = 'inventory_items'
    id = Column(Integer, primary_key=True)
    inventory_id = Column(Integer, ForeignKey('inventories.id'))
    item_id = Column(String)
    name = Column(String)
    item_type = Column(String)
    quantity = Column(Integer, default=1)
    inventory = relationship('Inventory', back_populates='items')
