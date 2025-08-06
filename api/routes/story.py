from fastapi import APIRouter
from api.models.story import StoryProgress

router = APIRouter()

# Consultar progreso narrativo del jugador
@router.get("/story/{player_id}/progress")
def get_story_progress(player_id: str):
    # TODO: Integrar con base de datos
    return {
        "player_id": player_id,
        "act": 1,
        "chapter": "El Rito y la Herida",
        "completed_missions": [],
        "current_mission": None,
        "logros": [],
        "narrative_flags": {}
    }

# Actualizar progreso narrativo
@router.post("/story/{player_id}/progress")
def update_story_progress(player_id: str, progress: StoryProgress):
    # TODO: Integrar con base de datos
    return {"status": "updated", "player_id": player_id, "progress": progress}

# Consultar log de eventos narrativos
@router.get("/story/{player_id}/log")
def get_story_log(player_id: str):
    # TODO: Integrar con base de datos
    return {"player_id": player_id, "log": []}
