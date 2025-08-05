from sqlalchemy import Column, Integer, String, ForeignKey, ARRAY, Float
from sqlalchemy.orm import relationship
from core.database import Base

class Sicario(Base):
    __tablename__ = "sicarios"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True)
    user = relationship("User")
    price = Column(Float, nullable=False)
    description = Column(String, nullable=True)
    is_available = Column(Integer, default=1)  # 1 = available, 0 = hired
    battle_history = Column(ARRAY(String), default=[])
    # Optionally: skills, reputation, etc.
