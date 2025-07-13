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
        abilities=['Bendición Divina', 'Escudo Sagrado'],
        special_attack='Llamado Celestial'
    ),
    'Sarracenos': Faction(
        name='Sarracenos',
        color=color.green,
        abilities=['Tormenta de Arena', 'Ilusión del Desierto'],
        special_attack='Furia del Jinn'
    ),
    'Antiguos': Faction(
        name='Antiguos',
        color=color.purple,
        abilities=['Manipulación de Sombras', 'Pacto Ancestral'],
        special_attack='Invocación del Dios Olvidado'
    )
}