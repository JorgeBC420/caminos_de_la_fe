from pydantic import BaseModel
from typing import Optional, List

class BlacksmithAction(BaseModel):
    user_id: int
    item_id: int
    action: str  # "forge", "upgrade", "repair"
    materials: Optional[List[str]] = None

class StableAction(BaseModel):
    user_id: int
    mount_type: str
    action: str  # "buy", "upgrade", "heal"
    mount_id: Optional[int] = None

class AlchemistAction(BaseModel):
    user_id: int
    potion_type: str
    action: str  # "brew", "upgrade", "purify"
    ingredients: Optional[List[str]] = None

class TavernAction(BaseModel):
    user_id: int
    action: str  # "rest", "gather_info", "recruit"
    target_id: Optional[int] = None
