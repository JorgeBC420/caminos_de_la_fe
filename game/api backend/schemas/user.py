from pydantic import BaseModel

class UserCreate(BaseModel):
    username: str
    password: str

class UserOut(BaseModel):
    username: str
    xp: int
    inventory: list[str]
    mission_progress: dict
    faction: str | None = None
    power_score: int = 0
    last_contribution_date: str | None = None
    ultimate_skill: str | None = None
