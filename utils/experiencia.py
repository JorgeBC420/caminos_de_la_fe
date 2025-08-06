def experiencia_requerida(nivel_actual: int) -> int:
    """
    Calcula la experiencia total requerida para alcanzar un nivel dado.
    Fórmula: experiencia = nivel_actual * (nivel_actual * 10)
    """
    return nivel_actual * (nivel_actual * 10)

# Ejemplos de uso
if __name__ == "__main__":
    for nivel in [1, 2, 5, 15, 50, 75, 100]:
        print(f"Nivel {nivel}: {experiencia_requerida(nivel)} experiencia total")
