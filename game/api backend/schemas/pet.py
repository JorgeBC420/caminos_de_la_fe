from pydantic import BaseModel
from typing import Optional, Dict, List

class PetSchema(BaseModel):
    id: int
    owner_id: int
    pet_type: str
    tier: str
    faction: Optional[str]
    stats: Dict[str, int]
    skills: List[str]
    level: int
    exp: int
    exp_to_next: int
    in_nursery: int
    shelter_timestamp: int
