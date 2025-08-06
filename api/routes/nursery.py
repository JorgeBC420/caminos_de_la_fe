from fastapi import APIRouter
from api.models.nursery import Nursery

router = APIRouter()

@router.get("/nursery/{player_id}")
def get_nursery(player_id: str):
    # TODO: Integrar con base de datos
    return {"player_id": player_id, "nursery": []}

# Endpoint para recoger mascota de la guardería
@router.post("/nursery/{player_id}/retrieve")
def retrieve_pet_from_nursery(player_id: str, pet_id: str):
    # TODO: Integrar con base de datos
    return {"status": "retrieved", "player_id": player_id, "pet_id": pet_id}
