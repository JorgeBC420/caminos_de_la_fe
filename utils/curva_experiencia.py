def factor_xp(nivel: int) -> float:
    """
    Devuelve el factor de experiencia según el rango de nivel.
    """
    if 1 <= nivel <= 10:
        return 1.0
    elif 11 <= nivel <= 30:
        return 1.2
    elif 31 <= nivel <= 60:
        return 1.5
    elif 61 <= nivel <= 80:
        return 2.0
    elif 81 <= nivel <= 100:
        return 2.5
    elif 101 <= nivel <= 120:
        return 3.0
    else:
        raise ValueError("Nivel fuera de rango (1-120)")


def xp_para_subir_nivel(nivel: int) -> int:
    """
    Calcula la experiencia necesaria para subir de nivel, según la curva escalonada.
    """
    return int(nivel * (nivel * 10) * factor_xp(nivel))


def xp_total_acumulada(nivel: int) -> int:
    """
    Calcula la experiencia total acumulada para alcanzar un nivel dado.
    """
    return sum(xp_para_subir_nivel(n) for n in range(1, nivel + 1))


# Ejemplo de desglose por nivel
if __name__ == "__main__":
    print("Nivel\tXP Nivel\tXP Total\tDías (800/día)\tDías (900/día)")
    for nivel in [10, 20, 50, 80, 100, 120]:
        xp_nivel = xp_para_subir_nivel(nivel)
        xp_total = xp_total_acumulada(nivel)
        dias_800 = round(xp_total / 800, 2)
        dias_900 = round(xp_total / 900, 2)
        print(f"{nivel}\t{xp_nivel}\t{xp_total}\t{dias_800}\t{dias_900}")
