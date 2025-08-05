
# Lógica de combate principal
from data.deity_data import DEITY_BONUSES

def calculate_damage(player, enemy, skill_name=None):
    """
    Calcula el daño considerando equipo avanzado y habilidades activas.
    Si skill_name está presente, aplica el efecto de la habilidad.
    """
    base_damage = getattr(player.stats, 'attack_power', 10)
    damage = base_damage
    # Bonificaciones de equipo avanzado
    if hasattr(player, 'advanced_gear') and player.advanced_gear:
        gear = player.advanced_gear.get('weapon', {})
        damage += gear.get('damage', 0)
        damage += gear.get('magic_damage', 0)
        damage += gear.get('critical', 0)
    # Habilidad activa
    if skill_name:
        # Buscar la habilidad en las skills de la facción
        faction = getattr(player, 'faction', None)
        deity = getattr(player, 'deity', None)
        skills = []
        if faction in DEITY_BONUSES:
            skills = DEITY_BONUSES[faction].get('skills', [])
        elif deity in DEITY_BONUSES:
            skills = DEITY_BONUSES[deity].get('skills', [])
        for skill in skills:
            if skill.get('name') == skill_name:
                # Ejemplo de efectos: Furia Berserker duplica daño
                if 'berserker' in skill_name.lower():
                    damage *= 2
                if 'divino' in skill_name.lower():
                    damage += 50
                if 'sandstorm' in skill_name.lower() or 'llamarada' in skill_name.lower():
                    damage += 30
                # Puedes expandir con más efectos
    # Defensa enemiga
    defense = getattr(enemy, 'defense', 5)
    final_damage = max(1, damage - defense)
    return final_damage

def apply_advanced_gear(player):
    """
    Aplica bonificaciones de equipo avanzado al jugador.
    """
    if hasattr(player, 'advanced_gear') and player.advanced_gear:
        gear = player.advanced_gear
        if 'armor' in gear:
            player.stats.defense += gear['armor'].get('defense', 0)
            player.stats.cold_resist = gear['armor'].get('cold_resist', 0)
            player.stats.magic_resist = gear['armor'].get('magic_resist', 0)
            player.stats.speed += gear['armor'].get('speed', 0)
        if 'weapon' in gear:
            player.stats.attack_power += gear['weapon'].get('damage', 0)
            player.stats.magic_damage = gear['weapon'].get('magic_damage', 0)
            player.stats.critical = gear['weapon'].get('critical', 0)

def use_skill_in_combat(player, enemy, skill_name):
    """
    Activa una habilidad avanzada durante el combate.
    """
    damage = calculate_damage(player, enemy, skill_name)
    enemy.health -= damage
    print(f"{player.name} usó {skill_name} e hizo {damage} de daño a {enemy.name}")
    # Aquí puedes agregar efectos visuales, estados, etc.
