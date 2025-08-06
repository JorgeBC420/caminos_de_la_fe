from fastapi import APIRouter, Depends
from schemas.city import StableAction
router = APIRouter(prefix="/stable", tags=["stable"])

@router.post("/action")
def stable_action(action: StableAction):
    # Simulación de lógica de establo
    return {"success": True, "action": action}
