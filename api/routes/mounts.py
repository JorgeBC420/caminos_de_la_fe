from fastapi import APIRouter
from api.models.mount import Mount

router = APIRouter()

@router.get("/mounts/{player_id}")
def get_mounts(player_id: str):
    # TODO: Integrar con base de datos
    return {"player_id": player_id, "mounts": []}
