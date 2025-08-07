FORTALEZA_COSTOS = [
    5000,    # Nivel 1
    10000,   # Nivel 2
    15000,   # Nivel 3
    20000,   # Nivel 4
    25000,   # Nivel 5
    30000,   # Nivel 6
    40000,   # Nivel 7
    50000,   # Nivel 8
    60000,   # Nivel 9
    70000,   # Nivel 10
    80000,   # Nivel 11
    90000,   # Nivel 12
    100000   # Nivel 13
]

# Tabla de costos de mejora de Casa/Hogar (niveles 1-40)
HOGAR_COSTOS = [
    100
]
# Progresión exponencial suave para casa: nivel 1=100, nivel 40=100000
for lvl in range(2, 41):
    # Fórmula: costo = 100 * (lvl ** 2.1) (ajustado para llegar a ~100,000 en nivel 40)
    costo = int(100 * (lvl ** 2.1))
    if costo > 100000:
        costo = 100000
    HOGAR_COSTOS.append(costo)
from enum import Enum

class BrotherhoodRole(Enum):
    RECLUTA = 1
    MIEMBRO = 2
    OFICIAL = 3
    LIDER = 4

PERMISSIONS = {
    BrotherhoodRole.LIDER: ['invitar', 'expulsar', 'ascender', 'degradar', 'cambiar_motd', 'retirar_tesoro'],
    BrotherhoodRole.OFICIAL: ['invitar', 'expulsar_reclutas', 'cambiar_motd'],
    BrotherhoodRole.MIEMBRO: ['donar'],
    BrotherhoodRole.RECLUTA: [],
}
