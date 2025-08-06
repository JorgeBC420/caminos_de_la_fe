from pydantic import BaseModel
from typing import Optional

class Mount(BaseModel):
    id: str
    owner_id: str
    mount_type: str
    speed_bonus: float = 2.0
    model: str = 'cube'
    color: Optional[str] = None
    active: bool = False
