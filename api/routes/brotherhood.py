# Migración desde clan.py

from fastapi import APIRouter

router = APIRouter()

@router.get("/brotherhoods")
def get_brotherhoods():
    return {"brotherhoods": []}
