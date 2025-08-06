from fastapi import APIRouter
from core.xp_curve import xp_curve_table

router = APIRouter(prefix="/xp_curve", tags=["xp_curve"])

@router.get("/", response_model=list)
def get_xp_curve():
    return xp_curve_table()
