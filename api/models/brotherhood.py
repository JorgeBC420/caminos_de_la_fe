from pydantic import BaseModel

class Brotherhood(BaseModel):
    name: str
    members: list
