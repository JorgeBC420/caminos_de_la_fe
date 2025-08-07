from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.postgresql import ARRAY

Base = declarative_base()

class Brotherhood(Base):
    __tablename__ = "brotherhoods"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    description = Column(String)
    members = Column(ARRAY(Integer), default=[])
    pending_invitations = Column(ARRAY(Integer), default=[])
    treasury = Column(Integer, default=0)
    fortress_level = Column(Integer, default=1)
    max_members = Column(Integer, default=25)
    general_id = Column(Integer, default=None)  # General (líder)
    guardian_ids = Column(ARRAY(Integer), default=[])
    donation_history = Column(ARRAY(Integer), default=[])
    returned_history = Column(ARRAY(Integer), default=[])
    fortress_expansions = Column(ARRAY(String), default=[])
    stolen_resources = Column(Integer, default=0)
    hired_sicarios = Column(ARRAY(Integer), default=[])
    legendary_weapon = Column(String, default=None)
    legendary_item = Column(String, default=None)
    # ...otros campos para expansión...

class BrotherhoodModel:
    def __init__(self, name, members):
        self.name = name
        self.members = members
