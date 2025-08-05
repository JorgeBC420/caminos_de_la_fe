# Definiciones de facciones y habilidades
from ursina import color

class Faction:
    def __init__(self, name, color, abilities, special_attack):
        self.name = name
        self.color = color
        self.abilities = abilities
        self.special_attack = special_attack

FACTIONS = {
    'Cruzados': Faction(
        name='Cruzados',
        color=color.gold,
        abilities=['Bendición Divina', 'Escudo Sagrado', 'Lanza de Gloria'],
        special_attack='Llamado Celestial'
    ),
    'Sarracenos': Faction(
        name='Sarracenos',
        color=color.green,
        abilities=['Tormenta de Arena', 'Ilusión del Desierto', 'Viento Envenenado'],
        special_attack='Furia del Jinn'
    ),
    'Antiguos': Faction(
        name='Antiguos',
        color=color.magenta,
        abilities=['Manipulación de Sombras', 'Pacto Ancestral', 'Susurro del Vacío'],
        special_attack='Invocación del Dios Olvidado'
    ),
    'Egipcios': Faction(
        name='Egipcios',
        color=color.yellow,
        abilities=['Veneno del Nilo', 'Bendición de Isis', 'Furia de Horus'],
        special_attack='Juicio de Anubis'  # Ultimate: daño masivo, debuff, curación
    ),
    'Romanos': Faction(
        name='Romanos',
        color=color.red,
        abilities=['Formación Legionaria', 'Disciplina de Combate', 'Gloria Imperial'],
        special_attack='Maremoto de Neptuno'  # Ultimate: AOE, buff aliados, control
    ),
    'Vikingos': Faction(
        name='Vikingos',
        color=color.cyan,
        abilities=['Congelación Nórdica', 'Relámpago de Thor', 'Modo Berserker'],
        special_attack='Ragnarok'  # Ultimate: furia, control, daño masivo
    ),
    'Griegos': Faction(
        name='Griegos',
        color=color.azure,
        abilities=['Relámpago de Zeus', 'Curación de Asclepio', 'Escudo Olímpico'],
        special_attack='Juicio del Olimpo'  # Ultimate: relámpago, curación, escudo divino
    )
}

# --- Roles y conceptos actualizados ---
# Guerra de Fe: Evento global de facciones
# Hermandad: Conjunto de jugadores (guild/clan)
# Sicarios: Jugadores mercenarios que luchan por oro en guerras de hermandad