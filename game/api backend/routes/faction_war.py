from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from models.user import User
from schemas.user import UserOut
from core.database import get_db
from core.auth import get_current_user
from datetime import datetime

router = APIRouter()

# Estado actual de la guerra de facciones (simulado)
FACTION_WAR_STATE = {
    "status": "active",
    "scores": {"Cruzados": 12000, "Sarracenos": 11000},
    "time_remaining": "12:34:56"
}

@router.get("/current_war", response_model=dict)
def get_current_war_status():
    return FACTION_WAR_STATE

@router.post("/submit_power")
def submit_player_power(
    faction: str,
    power: int,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user)
):
    today = datetime.now().date().isoformat()
    if user.last_contribution_date == today:
        raise HTTPException(status_code=400, detail="Ya contribuiste hoy")
    user.faction = faction
    user.power_score = power
    user.last_contribution_date = today
    db.commit()
    FACTION_WAR_STATE["scores"][faction] = FACTION_WAR_STATE["scores"].get(faction, 0) + power
    return {"success": True, "power": power}
