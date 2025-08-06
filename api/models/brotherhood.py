from pydantic import BaseModel

class Brotherhood(BaseModel):
    id: str
    name: str
    description: str = ""
    members: list[str] = []
