from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.postgresql import ARRAY, JSON

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    xp = Column(Integer, default=0)
    inventory = Column(ARRAY(String), default=[])
    mission_progress = Column(JSON, default={})
    faction = Column(String, default=None)
    power_score = Column(Integer, default=0)
    last_contribution_date = Column(String, default=None)  # ISO date string
    ultimate_skill = Column(String, default=None)  # Habilidad definitiva elegida
