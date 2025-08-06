from fastapi import APIRouter
from api.models.player import Player

router = APIRouter()

@router.get("/player/{player_id}")
def get_player(player_id: str):
    # TODO: Integrar con base de datos
    return {"player_id": player_id, "player": {}}
