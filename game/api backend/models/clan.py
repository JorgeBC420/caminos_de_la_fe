from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.postgresql import ARRAY

Base = declarative_base()

class Clan(Base):
    __tablename__ = "clans"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    description = Column(String)
    leader_id = Column(Integer, ForeignKey("users.id"))
    leader = relationship("User")
    general_id = Column(Integer, ForeignKey("users.id"))
    general = relationship("User", foreign_keys=[general_id])
    guardian_ids = Column(ARRAY(Integer))  # Up to 5 user IDs
    legendary_item = Column(String, nullable=True)
    legendary_weapon = Column(String, nullable=True)
    members = Column(ARRAY(Integer), default=[])
    pending_invitations = Column(ARRAY(Integer), default=[])
