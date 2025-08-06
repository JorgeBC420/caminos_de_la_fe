from fastapi import APIRouter, Depends
from schemas.city import TavernAction
router = APIRouter(prefix="/tavern", tags=["tavern"])

@router.post("/action")
def tavern_action(action: TavernAction):
    # Simulación de lógica de taberna
    return {"success": True, "action": action}
