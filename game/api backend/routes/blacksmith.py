from fastapi import APIRouter, Depends
from schemas.city import BlacksmithAction
router = APIRouter(prefix="/blacksmith", tags=["blacksmith"])

@router.post("/action")
def blacksmith_action(action: BlacksmithAction):
    # Simulación de lógica de herrero
    return {"success": True, "action": action}
