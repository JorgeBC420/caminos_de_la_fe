from pydantic import BaseModel
from typing import List, Optional

class Nursery(BaseModel):
    owner_id: str
    slots: List[str] = []  # pet ids
    max_slots: int = 2
    timestamp: Optional[int] = None
