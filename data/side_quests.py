# Misiones secundarias repetitivas
SIDE_QUESTS = [
    {
        'key': 'limpiar_calabozo',
        'name': 'Limpiar Calabozo',
        'description': 'Elimina a todos los enemigos en el calabozo.',
        'reward': {'xp': 50, 'gold': 30, 'item': None},
        'repeatable': True
    },
    {
        'key': 'conseguir_medicinas',
        'name': 'Conseguir Medicinas',
        'description': 'Recolecta hierbas y entrega medicinas en el Hospital.',
        'reward': {'xp': 40, 'gold': 20, 'item': 'medicina'},
        'repeatable': True
    },
    {
        'key': 'llevar_enfermos',
        'name': 'Llevar Enfermos al Hospital',
        'description': 'Transporta enfermos al Hospital antes de que se acabe el tiempo.',
        'reward': {'xp': 60, 'gold': 25, 'item': None},
        'repeatable': True
    },
    {
        'key': 'escoltar_caravana',
        'name': 'Escoltar Caravana',
        'description': 'Protege la caravana hasta su destino. +moral, -dinero, recompensa adicional aleatoria.',
        'reward': {'xp': 70, 'gold': 10, 'item': 'recompensa_aleatoria', 'moral': 5},
        'repeatable': True
    },
    {
        'key': 'asaltar_caravana',
        'name': 'Asaltar Caravana',
        'description': 'Ataca la caravana y roba sus bienes. -moral, +dinero.',
        'reward': {'xp': 50, 'gold': 60, 'item': None, 'moral': -10},
        'repeatable': True
    },
    {
        'key': 'guardaespaldas',
        'name': 'Guardaespaldas',
        'description': 'Protege a un personaje importante durante su viaje.',
        'reward': {'xp': 80, 'gold': 35, 'item': None},
        'repeatable': True
    }
]
