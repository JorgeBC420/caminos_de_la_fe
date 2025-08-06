"""
Este archivo ha sido migrado. Usar schemas/brotherhood.py para las definiciones de hermandad.
"""
from pydantic import BaseModel
from typing import Optional, List

class BrotherhoodBase(BaseModel):
    name: str
    description: Optional[str] = None
    general_id: Optional[int] = None
    guardian_ids: Optional[List[int]] = []
    legendary_item: Optional[str] = None
    legendary_weapon: Optional[str] = None
    members: Optional[List[int]] = []
    pending_invitations: Optional[List[int]] = []

class BrotherhoodCreate(BrotherhoodBase):
    pass

class BrotherhoodOut(BrotherhoodBase):
    id: int
    leader_id: int
    members: Optional[List[int]] = []
    pending_invitations: Optional[List[int]] = []
    class Config:
        orm_mode = True
