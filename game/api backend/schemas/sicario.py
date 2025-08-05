from pydantic import BaseModel
from typing import Optional, List

class SicarioBase(BaseModel):
    user_id: int
    price: float
    description: Optional[str] = None
    is_available: Optional[int] = 1
    battle_history: Optional[List[str]] = []

class SicarioCreate(SicarioBase):
    pass

class SicarioOut(SicarioBase):
    id: int
    class Config:
        orm_mode = True
