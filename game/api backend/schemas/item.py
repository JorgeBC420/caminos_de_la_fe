from pydantic import BaseModel
from typing import Optional, Dict, List

class ItemSchema(BaseModel):
    id: int
    name: str
    type: str
    rarity: str
    description: Optional[str]
    stats: Optional[Dict[str, int]]
    effects: Optional[List[str]]

class InventorySchema(BaseModel):
    user_id: int
    items: List[ItemSchema]

class UltimateSkillSchema(BaseModel):
    name: str
    type: str
    desc: str
    faction: str
