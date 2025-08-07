from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from .base import Base

class Player(Base):
    __tablename__ = 'players'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    faction = Column(String)
    level = Column(Integer, default=1)
    exp = Column(Integer, default=0)
    # Relaciones: inventario, mascotas, monturas, armas, etc. pueden agregarse aquí
