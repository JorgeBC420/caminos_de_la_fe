from pydantic import BaseModel
from typing import Optional

class Weapon(BaseModel):
    id: str
    owner_id: str
    weapon_type: str
    rarity: str
    stats: dict
    skills: Optional[list] = []
    equipped: bool = False
