from fastapi import APIRouter, Depends
from schemas.city import AlchemistAction
router = APIRouter(prefix="/alchemist", tags=["alchemist"])

@router.post("/action")
def alchemist_action(action: AlchemistAction):
    # Simulación de lógica de alquimista
    return {"success": True, "action": action}
