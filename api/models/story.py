from pydantic import BaseModel
from typing import Optional, List

class StoryProgress(BaseModel):
    player_id: str
    act: int
    chapter: str
    completed_missions: List[str] = []
    current_mission: Optional[str] = None
    logros: List[str] = []
    narrative_flags: dict = {}
