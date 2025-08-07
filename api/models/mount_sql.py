from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base

class Mount(Base):
    __tablename__ = 'mounts'
    id = Column(Integer, primary_key=True, index=True)
    owner_id = Column(Integer, ForeignKey('players.id'))
    mount_type = Column(String, index=True)
    speed_bonus = Column(Float, default=2.0)
    model = Column(String, default='cube')
    color = Column(String, nullable=True)
    active = Column(Boolean, default=False)
    # Relationship to Player (optional, for backref)
    # owner = relationship('Player', back_populates='mounts')
