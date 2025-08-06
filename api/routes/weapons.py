from fastapi import APIRouter
from api.models.weapon import Weapon

router = APIRouter()

@router.get("/weapons/{player_id}")
def get_weapons(player_id: str):
    # TODO: Integrar con base de datos
    return {"player_id": player_id, "weapons": []}
