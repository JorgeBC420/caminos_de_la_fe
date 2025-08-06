from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from models.user import User
from core.database import get_db
from core.auth import get_current_user
import random

router = APIRouter(prefix="/pvp", tags=["pvp"])

# Configuración de recompensas PvP
PVP_REWARD_XP_WIN = 300
PVP_REWARD_XP_LOSE = 100
PVP_REWARD_GOLD_WIN = 150
PVP_REWARD_GOLD_LOSE = 50

@router.post("/duel")
def start_duel(
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
    opponent_id: int = None
):
    # Simulación avanzada de stats (usar stats reales si están en el modelo)
    user_stats = {
        "nivel": getattr(user, "level", 10),
        "fuerza": getattr(user, "strength", 100),
        "agilidad": getattr(user, "agility", 80),
        "defensa": getattr(user, "defense", 90),
        "resistencia": getattr(user, "vitality", 100)
    }
    # Simular o buscar oponente
    opponent_stats = {
        "nivel": 10,
        "fuerza": 95,
        "agilidad": 85,
        "defensa": 88,
        "resistencia": 100
    }
    user_hp = 1000 + user_stats["resistencia"] * 5
    opponent_hp = 1000 + opponent_stats["resistencia"] * 5
    rounds = []
    protection = False
    # Cooldown de habilidades
    base_ulti_cd = 8
    ulti_cd = max(3, base_ulti_cd - user_stats["nivel"] // 10)
    basic_cd = 3
    next_ulti = ulti_cd
    next_basic = basic_cd
    for i in range(1, 11):
        # Ataque del oponente
        if random.random() < user_stats["agilidad"] / (200 + user_stats["nivel"]):
            rounds.append(f"Ronda {i}: Evadiste el ataque enemigo.")
        else:
            dmg = max(0, opponent_stats["fuerza"] + opponent_stats["nivel"] - user_stats["defensa"] // 2)
            user_hp -= dmg
            rounds.append(f"Ronda {i}: Recibiste {dmg} de daño.")
        # Contragolpe
        if random.random() < user_stats["fuerza"] / (200 + opponent_stats["nivel"]):
            dmg = max(0, user_stats["fuerza"] + user_stats["nivel"] - opponent_stats["defensa"] // 2)
            opponent_hp -= dmg
            rounds.append(f"Ronda {i}: Contragolpeaste y causaste {dmg} de daño.")
        else:
            rounds.append(f"Ronda {i}: El rival evadió tu ataque.")
        # Habilidad básica
        if next_basic == 0:
            basic_dmg = int(user_stats["fuerza"] * 0.7)
            opponent_hp -= basic_dmg
            rounds.append(f"Ronda {i}: Activaste habilidad básica y causaste {basic_dmg} de daño.")
            next_basic = basic_cd
        else:
            next_basic -= 1
        # Ulti
        if next_ulti == 0:
            ulti_dmg = int(user_stats["fuerza"] * 1.5 + user_stats["nivel"] * 2)
            opponent_hp -= ulti_dmg
            rounds.append(f"Ronda {i}: ¡ULTI activada! Causaste {ulti_dmg} de daño.")
            next_ulti = ulti_cd
        else:
            next_ulti -= 1
        # Fin por debilitamiento
        if user_hp <= 0.75 * (1000 + user_stats["resistencia"] * 5):
            protection = True
            rounds.append(f"Has sido debilitado un 25%. Activada protección temporal.")
            break
        if opponent_hp <= 0.75 * (1000 + opponent_stats["resistencia"] * 5):
            rounds.append(f"El rival ha sido debilitado un 25%. Ganas la batalla.")
            break
    result = "win" if opponent_hp < user_hp else "lose"
    # Recompensas y protección
    if result == "win":
        user.xp += PVP_REWARD_XP_WIN
        user.inventory.append("Oro: %d" % PVP_REWARD_GOLD_WIN)
        db.commit()
        return {
            "result": "win",
            "xp_gained": PVP_REWARD_XP_WIN,
            "gold_gained": PVP_REWARD_GOLD_WIN,
            "battle_log": rounds,
            "protection": protection
        }
    else:
        user.xp += PVP_REWARD_XP_LOSE
        user.inventory.append("Oro: %d" % PVP_REWARD_GOLD_LOSE)
        db.commit()
        return {
            "result": "lose",
            "xp_gained": PVP_REWARD_XP_LOSE,
            "gold_gained": PVP_REWARD_GOLD_LOSE,
            "battle_log": rounds,
            "protection": protection
        }
