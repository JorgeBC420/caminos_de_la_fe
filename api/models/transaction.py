from sqlalchemy import Column, Integer, String, ForeignKey, Float, DateTime
from sqlalchemy.orm import relationship
from .base import Base
import datetime

class Transaction(Base):
    __tablename__ = 'transactions'
    id = Column(Integer, primary_key=True)
    player_id = Column(Integer, ForeignKey('players.id'))
    item_id = Column(String)
    item_name = Column(String)
    item_type = Column(String)
    price = Column(Float)
    quantity = Column(Integer, default=1)
    transaction_type = Column(String)  # 'buy' or 'sell'
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)
