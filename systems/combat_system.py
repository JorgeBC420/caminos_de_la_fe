# combat_system.py

def calculate_damage(attacker, defender):
    # Ejemplo simple: daño base + fuerza - defensa
    base_damage = getattr(attacker, 'attack_damage', 10)
    strength = getattr(attacker, 'stats', {}).get('fuerza', 0) if hasattr(attacker, 'stats') else 0
    defense = getattr(defender, 'stats', {}).get('defensa', 0) if hasattr(defender, 'stats') else 0
    damage = base_damage + strength - defense
    return max(1, damage)
