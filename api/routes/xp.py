from fastapi import APIRouter

router = APIRouter()

def xp_for_level(level: int) -> int:
    if 1 <= level <= 10:
        factor = 1.0
    elif 11 <= level <= 30:
        factor = 1.2
    elif 31 <= level <= 60:
        factor = 1.5
    elif 61 <= level <= 80:
        factor = 2.0
    elif 81 <= level <= 100:
        factor = 2.5
    elif 101 <= level <= 120:
        factor = 3.0
    else:
        factor = 3.0
    return int(level * (level * 10) * factor)

@router.get("/xp/level/{level}")
def get_xp_for_level(level: int):
    xp = xp_for_level(level)
    return {"level": level, "xp_required": xp}
