from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from models.user import User
from core.database import get_db
from core.auth import get_current_user
from datetime import datetime

router = APIRouter()

# Simulación de recompensas diarias
DAILY_REWARDS = [
    {"gold": 100, "item": "Poción Pequeña"},
    {"gold": 200, "item": "Llave de Cofre"},
    {"gold": 300, "item": "Token de Facción"},
    {"gold": 400, "item": None},
    {"gold": 500, "item": "Poción Grande"},
]

@router.post("/claim_daily_reward")
def claim_daily_reward(
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user)
):
    today = datetime.now().date().isoformat()
    if user.last_contribution_date == today:
        raise HTTPException(status_code=400, detail="Ya reclamaste la recompensa hoy")
    streak = user.xp % len(DAILY_REWARDS)
    reward = DAILY_REWARDS[streak]
    # Simulación: sumar oro y agregar item al inventario
    user.inventory.append(reward["item"]) if reward["item"] else None
    user.xp += reward["gold"]
    user.last_contribution_date = today
    db.commit()
    return {"success": True, "reward": reward}
