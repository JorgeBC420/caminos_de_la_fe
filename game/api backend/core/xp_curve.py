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
        raise ValueError("Nivel fuera de rango")
    return int(level * (level * 10) * factor)

def xp_curve_table(max_level: int = 120) -> list:
    curve = []
    total = 0
    for lvl in range(1, max_level + 1):
        xp = xp_for_level(lvl)
        total += xp
        curve.append({
            "level": lvl,
            "xp_for_level": xp,
            "total_xp": total
        })
    return curve
