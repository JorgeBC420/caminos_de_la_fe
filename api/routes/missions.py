from fastapi import APIRouter
from api.models.mission import MissionStory

router = APIRouter()

# Obtener misiones activas y completadas de un jugador
@router.get("/missions/{player_id}")
def get_missions(player_id: str):
    # TODO: Integrar con base de datos
    return {"player_id": player_id, "missions": []}

# Crear nueva misión
@router.post("/missions/")
def create_mission(mission: MissionStory):
    # TODO: Integrar con base de datos
    return {"status": "created", "mission": mission}

# Completar misión
@router.post("/missions/{mission_id}/complete")
def complete_mission(mission_id: str):
    # TODO: Integrar con base de datos
    return {"status": "completed", "mission_id": mission_id}

# Marcar misión como fallida
@router.post("/missions/{mission_id}/fail")
def fail_mission(mission_id: str):
    # TODO: Integrar con base de datos
    return {"status": "failed", "mission_id": mission_id}
