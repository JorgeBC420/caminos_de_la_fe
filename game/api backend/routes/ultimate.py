from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from models.user import User
from core.database import get_db
from core.auth import get_current_user
from data.ultimate_skills import ULTIMATE_SKILLS

router = APIRouter()

@router.get("/ultimate_skills/{faction}")
def get_ultimate_skills(faction: str):
    skills = ULTIMATE_SKILLS.get(faction)
    if not skills:
        raise HTTPException(status_code=404, detail="Facción no encontrada")
    return skills

@router.post("/choose_ultimate")
def choose_ultimate(
    skill_name: str,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user)
):
    # Validar que la habilidad existe para la facción del usuario
    faction = user.faction
    valid_skills = [s['name'] for s in ULTIMATE_SKILLS.get(faction, [])]
    if skill_name not in valid_skills:
        raise HTTPException(status_code=400, detail="Habilidad no válida para tu facción")
    user.ultimate_skill = skill_name
    db.commit()
    return {"success": True, "ultimate_skill": skill_name}
