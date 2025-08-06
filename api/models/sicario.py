from pydantic import BaseModel

class Sicario(BaseModel):
    id: str
    name: str
    skill: str = ""
    hired: bool = False
