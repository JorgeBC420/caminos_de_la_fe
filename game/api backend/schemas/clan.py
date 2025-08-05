from pydantic import BaseModel
from typing import Optional, List

class ClanBase(BaseModel):
    name: str
    description: Optional[str] = None
    general_id: Optional[int] = None
    guardian_ids: Optional[List[int]] = []
    legendary_item: Optional[str] = None
    legendary_weapon: Optional[str] = None
    members: Optional[List[int]] = []
    pending_invitations: Optional[List[int]] = []

class ClanCreate(ClanBase):
    pass

class ClanOut(ClanBase):
    id: int
    leader_id: int
    members: Optional[List[int]] = []
    pending_invitations: Optional[List[int]] = []
    class Config:
        orm_mode = True
