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
