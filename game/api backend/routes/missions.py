from fastapi import APIRouter, Depends, HTTPException
from models.user import User
from sqlalchemy.orm import Session
from core.database import SessionLocal
import json
import os
from typing import List, Optional

router = APIRouter(prefix="/missions", tags=["missions"])

TUTORIAL_PATH = os.path.join(os.path.dirname(__file__), '../client/data/missions/mission_tutorial.json')
STORY_PATH = os.path.join(os.path.dirname(__file__), '../client/data/missions/mission_story.json')
SIDE_PATH = os.path.join(os.path.dirname(__file__), '../client/data/missions/mission_side.json')

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Listar misiones por tipo
@router.get("/tutorial", response_model=List[dict])
def list_tutorial_missions():
    try:
        with open(TUTORIAL_PATH, 'r', encoding='utf-8') as f:
            missions = json.load(f)
    except Exception:
        missions = []
    return missions

@router.get("/story", response_model=List[dict])
def list_story_missions():
    try:
        with open(STORY_PATH, 'r', encoding='utf-8') as f:
            missions = json.load(f)
    except Exception:
        missions = []
    return missions

@router.get("/side", response_model=List[dict])
def list_side_missions():
    try:
        with open(SIDE_PATH, 'r', encoding='utf-8') as f:
            missions = json.load(f)
    except Exception:
        missions = []
    return missions


# Obtener misión por tipo e id
@router.get("/{mission_type}/{mission_id}", response_model=dict)
def get_mission(mission_type: str, mission_id: int):
    path_map = {
        "tutorial": TUTORIAL_PATH,
        "story": STORY_PATH,
        "side": SIDE_PATH
    }
    file_path = path_map.get(mission_type)
    if not file_path:
        raise HTTPException(status_code=400, detail="Tipo de misión inválido")
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            missions = json.load(f)
        if 0 <= mission_id < len(missions):
            return missions[mission_id]
    except Exception:
        pass
    raise HTTPException(status_code=404, detail="Mission not found")


# Completar misión por tipo e id
@router.post("/complete/{mission_type}/{mission_id}")
def complete_mission(mission_type: str, mission_id: int, user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    path_map = {
        "tutorial": TUTORIAL_PATH,
        "story": STORY_PATH,
        "side": SIDE_PATH
    }
    file_path = path_map.get(mission_type)
    if not file_path:
        raise HTTPException(status_code=400, detail="Tipo de misión inválido")
    with open(file_path, 'r', encoding='utf-8') as f:
        missions = json.load(f)
    if 0 <= mission_id < len(missions):
        mission = missions[mission_id]
        user.xp = getattr(user, 'xp', 0) + mission.get('xp_reward', 0)
        user.inventory = getattr(user, 'inventory', []) + mission.get('loot', [])
        db.commit()
        return {"detail": f"Misión {mission_id} completada para usuario {user_id}", "xp": user.xp, "loot": user.inventory}
    raise HTTPException(status_code=404, detail="Misión no encontrada")

@router.post("/progress/{mission_id}")
def update_mission_progress(mission_id: int, user_id: int, progress: dict, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    # Guardar progreso (simplificado)
    user.mission_progress = getattr(user, 'mission_progress', {})
    user.mission_progress[str(mission_id)] = progress
    db.commit()
    return {"detail": f"Progreso actualizado para misión {mission_id} y usuario {user_id}", "progress": user.mission_progress}
