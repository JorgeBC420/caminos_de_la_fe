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
from pydantic import BaseModel

class BrotherhoodSchema(BaseModel):
    id: int
    name: str
    description: str
    members: list[int]
    pending_invitations: list[int]
    treasury: int
    fortress_level: int
    max_members: int
    general_id: int | None
    guardian_ids: list[int]
    donation_history: list[int]
    returned_history: list[int]
    fortress_expansions: list[str]
    stolen_resources: int
    hired_sicarios: list[int]
    legendary_weapon: str | None
    legendary_item: str | None
    # ...otros campos para expansión...

    def __init__(self, name, members):
        self.name = name
        self.members = members
