# Diccionario de ítems legendarios y únicos por facción
# Cada entrada incluye atributos, lore y mecánicas especiales

LEGENDARY_ITEMS = {
    'Cruzados': {
        'name': 'Cáliz de la Salvación Eterna',
        'type': 'Joyería',
        'base_stats': {'vida_max': 0.01, 'curacion': 0.005},  # % por nivel
        'unique_mechanic': 'Resurrección Pasiva',
        'lore': "Tallado del madero del Arca de Noé, contiene una gota de sangre de Cristo. Solo el más puro de corazón puede portarlo sin sufrir combustión espiritual.",
        'visual': 'Aura dorada, partículas de cruces flotantes',
        'cooldown': 3600
    },
    'Sarracenos': {
        'name': 'Espejo de las Mil Lunas',
        'type': 'Accesorio',
        'base_stats': {'evasión': 0.02, 'daño_critico': 0.01},
        'unique_mechanic': 'Ilusión Maestra',
        'lore': "Forjado con arena de la tumba de Salomón, refleja el alma del portador. Quien se mire en él demasiado tiempo perderá su sombra... y su humanidad.",
        'visual': 'Espejismo, distorsión de aire',
        'cooldown': 1200
    },
    'Antiguos': {
        'name': 'Máscara del Dios Sin Rostro',
        'type': 'Casco',
        'base_stats': {'poder_habilidad': 0.03, 'penetracion': 0.01},
        'unique_mechanic': 'Dominación',
        'lore': "Último fragmento del ídolo de Baal, susurra secretos en lenguas muertas. Portarla más de una hora convierte la piel en piedra obsidiana.",
        'visual': 'Aura de sombras, ojos brillantes',
        'cooldown': 600
    }
}

# Ejemplo de función para calcular stats dinámicos

def calculate_item_stats(item, owner_level):
    stats = {}
    for k, v in item['base_stats'].items():
        stats[k] = int(owner_level * v * 100) / 100  # % por nivel
    return stats
