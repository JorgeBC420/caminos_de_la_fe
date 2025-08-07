# data/pet_data.py
# Mascotas con stats de NPC, progresión por misiones, guardería implementada

PET_DATA = {
    'lobo_de_guerra': {
        'name': 'Lobo de Guerra',
        'image_icon': 'assets/pet/lobo_icon.png',
        'image_full': 'assets/pet/lobo_full.png',
        'unlock_level': 1,
        'base_stats': {'vida': 120, 'daño': 15, 'velocidad': 7},
        'level': 1,
        'xp': 0,
        'xp_to_next': 100,
        'xp_curve': [100 + 20 * lvl for lvl in range(1, 21)],
    },
    'leon_de_la_alianza': {
        'name': 'León de la Alianza',
        'image_icon': 'assets/pet/leon_icon.png',
        'image_full': 'assets/pet/leon_full.png',
        'unlock_level': 10,
        'base_stats': {'vida': 200, 'daño': 20, 'velocidad': 6},
        'level': 1,
        'xp': 0,
        'xp_to_next': 120,
        'xp_curve': [120 + 25 * lvl for lvl in range(1, 21)],
    },
    'halcon_de_la_sombra': {
        'name': 'Halcón de la Sombra',
        'image_icon': 'assets/pet/halcon_icon.png',
        'image_full': 'assets/pet/halcon_full.png',
        'unlock_level': 15,
        'base_stats': {'vida': 90, 'daño': 25, 'velocidad': 10},
        'level': 1,
        'xp': 0,
        'xp_to_next': 140,
        'xp_curve': [140 + 30 * lvl for lvl in range(1, 21)],
    },
    'draco_esmeralda': {
        'name': 'Draco Esmeralda',
        'image_icon': 'assets/pet/draco_icon.png',
        'image_full': 'assets/pet/draco_full.png',
        'unlock_level': 30,
        'base_stats': {'vida': 300, 'daño': 40, 'velocidad': 8},
        'level': 1,
        'xp': 0,
        'xp_to_next': 200,
        'xp_curve': [200 + 40 * lvl for lvl in range(1, 21)],
    },
}
