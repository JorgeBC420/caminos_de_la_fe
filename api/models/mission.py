from pydantic import BaseModel
from typing import Optional, List

class MissionStory(BaseModel):
    id: str
    name: str
    description: str
    act: Optional[int] = None
    chapter: Optional[str] = None
    player_id: Optional[str] = None
    status: str = "active"  # active, completed, failed
    objectives: List[str] = []
    rewards: List[str] = []
    time_limit: Optional[int] = None  # segundos
    crisis: bool = False
