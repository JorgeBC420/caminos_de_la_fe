from pydantic import BaseModel
from typing import Dict, Optional

class Player(BaseModel):
    id: str
    name: str
    faction: str
    level: int
    exp: int
    pet_inventory: Dict[str, str] = {}
    mount_inventory: Dict[str, str] = {}
    weapon_inventory: Dict[str, str] = {}
    active_pet: Optional[str] = None
    active_mount: Optional[str] = None
    nursery_slots: Optional[list] = []
