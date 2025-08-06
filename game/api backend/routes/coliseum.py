
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from core.database import get_db

router = APIRouter(prefix="/coliseum", tags=["coliseum"])

# Crear reto/apuesta
@router.post("/challenge")
def create_challenge(challenger_id: int, opponent_id: int, gold_bet: int, db: Session = Depends(get_db)):
    # Aquí se guardaría el reto en la base de datos (simplificado)
    return {"success": True, "challenger": challenger_id, "opponent": opponent_id, "gold_bet": gold_bet}

# Aceptar reto
@router.post("/accept")
def accept_challenge(challenge_id: int, db: Session = Depends(get_db)):
    # Aquí se marcaría el reto como aceptado
    return {"success": True, "challenge_id": challenge_id, "accepted": True}

# Simular combate y entregar botín
@router.post("/fight")
def fight_coliseum(challenge_id: int, db: Session = Depends(get_db)):
    # Simulación básica: el ganador se decide aleatoriamente
    import random
    winner_id = random.choice([1, 2])  # 1: challenger, 2: opponent
    gold_bet = 100  # Aquí deberías obtener el valor real del reto
    experience = 50  # Experiencia base
    return {
        "success": True,
        "winner": winner_id,
        "gold_awarded": gold_bet,
        "experience_awarded": experience
    }
