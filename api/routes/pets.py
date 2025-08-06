from fastapi import APIRouter
from api.models.pet import Pet

router = APIRouter()

# Endpoint para obtener mascotas de un jugador
@router.get("/pets/{player_id}")
def get_pets(player_id: str):
    # TODO: Integrar con base de datos
    return {"player_id": player_id, "pets": []}

# Endpoint para activar mascota
@router.post("/pets/{player_id}/activate")
def activate_pet(player_id: str, pet_id: str):
    # TODO: Integrar con base de datos
    return {"status": "activated", "player_id": player_id, "pet_id": pet_id}

# Endpoint para enviar mascota a guardería
@router.post("/nursery/{player_id}")
def send_pet_to_nursery(player_id: str, pet_id: str):
    # TODO: Integrar con base de datos
    return {"status": "ok", "player_id": player_id, "pet_id": pet_id}

# Endpoint para subir de nivel mascota
@router.post("/pets/{player_id}/levelup")
def levelup_pet(player_id: str, pet_id: str):
    # TODO: Integrar con base de datos
    return {"status": "leveled_up", "player_id": player_id, "pet_id": pet_id}
