# Armas legendarias por facción
LEGENDARY_WEAPONS = {
    'cruzado': {
        'name': 'Espada del Juicio Final',
        'base_stats': {'damage': 1.3, 'defense': 1.15},
        'unique_skill': 'Luz Divina',
        'skill_desc': 'Ciega enemigos en área (3s, cooldown 60s)',
        'level_bonus': {'damage': 0.05, 'defense': 0.02},
    },
    'sarraceno': {
        'name': 'Cimitarra de los Cuatro Vientos',
        'base_stats': {'speed': 1.4, 'hp': 1.1},
        'unique_skill': 'Tormenta de Arena',
        'skill_desc': 'AOE con daño + ralentización',
        'level_bonus': {'speed': 0.04, 'hp': 0.03},
    },
    'antiguo': {
        'name': 'Guadaña del Olvido',
        'base_stats': {'damage': 1.25, 'lifesteal': 1.2},
        'unique_skill': 'Pacto Ancestral',
        'skill_desc': 'Invoca espectros al matar enemigos',
        'level_bonus': {'lifesteal': 0.06, 'specters': 1},
        'max_specters': 5,
    }
}

# Ítems únicos por facción (1 por servidor)
LEGENDARY_UNIQUES = {
    'cruzado': {
        'name': 'Cáliz de la Salvación Eterna',
        'dynamic_stats': {'max_hp': 0.01, 'regen': 0.005},
        'unique_mechanic': 'Resurrección Pasiva: revive con 30% vida (cooldown 1h)',
    },
    'sarraceno': {
        'name': 'Espejo de las Mil Lunas',
        'dynamic_stats': {'evasion': 0.02, 'crit': 0.01},
        'unique_mechanic': 'Ilusión Maestra: crea 2 clones (20% daño)',
    },
    'antiguo': {
        'name': 'Máscara del Dios Sin Rostro',
        'dynamic_stats': {'skill_power': 0.03, 'penetration': 0.01},
        'unique_mechanic': 'Dominación: controla enemigos no jugadores por 10s',
    }
}
