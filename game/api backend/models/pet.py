from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Pet(Base):
    __tablename__ = "pets"
    id = Column(Integer, primary_key=True, index=True)
    owner_id = Column(Integer, ForeignKey("users.id"))
    pet_type = Column(String)
    tier = Column(String)  # common, epic, legendary
    faction = Column(String, nullable=True)
    stats = Column(JSONB)  # health, damage, speed, etc.
    skills = Column(JSONB) # lista de skills
    level = Column(Integer, default=1)
    exp = Column(Integer, default=0)
    exp_to_next = Column(Integer, default=100)
    in_nursery = Column(Integer, default=0)  # 0: no, 1: sí
    shelter_timestamp = Column(Integer, default=0)
