from pydantic import BaseModel
from typing import Optional, List

class Pet(BaseModel):
    id: str
    owner_id: str
    pet_type: str
    tier: str
    faction: Optional[str]
    level: int = 1
    exp: int = 0
    exp_to_next: int = 100
    stats: dict
    skills: List[str] = []
    in_nursery: bool = False
    nursery_timestamp: Optional[int] = None
    inventory: dict = {}
    localization: dict = {
        "es": {},
        "en": {},
        "de": {},
        "fr": {},
        "it": {},
        "pt": {},
        "ar": {}
    }
