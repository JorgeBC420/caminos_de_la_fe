import random
from data.config import AutoCombatConfig

class AutoCombatSystem:
    def __init__(self, player):
        self.player = player

    def calculate_battle_outcome(self, enemy_power):
        player_power = self.calculate_player_power()
        faction_modifier = self.get_faction_modifier(enemy_power.get('faction', None))
        player_power *= faction_modifier
        luck_factor = self.calculate_luck_factor()
        effective_player_power = player_power * luck_factor
        effective_enemy_power = enemy_power['total'] * random.uniform(0.8, 1.2)
        return {
            'victory': effective_player_power > effective_enemy_power,
            'player_power': effective_player_power,
            'enemy_power': effective_enemy_power,
            'damage_taken': self.calculate_damage_taken(effective_enemy_power)
        }

    def calculate_player_power(self):
        base_power = (
            self.player.level * 10 +
            self.player.stats['strength'] * 2 +
            self.player.stats['defense'] * 1.5
        )
        for item in self.player.equipment.values():
            if item:
                base_power += item.power_rating
        return base_power

    def calculate_luck_factor(self):
        min_luck = max(0.9, 1.0 - (self.player.level * 0.01))
        max_luck = min(1.1, 1.0 + (self.player.level * 0.01))
        return random.uniform(min_luck, max_luck)

    def get_faction_modifier(self, enemy_faction):
        if not enemy_faction or not self.player.faction:
            return 1.0
        modifiers = {
            'Cruzados': {'Antiguos': 1.3, 'Sarracenos': 0.9},
            'Sarracenos': {'Cruzados': 1.2, 'Antiguos': 1.0},
            'Antiguos': {'Sarracenos': 1.1, 'Cruzados': 0.8}
        }
        return modifiers.get(self.player.faction.name, {}).get(enemy_faction, 1.0)

    def calculate_damage_taken(self, effective_enemy_power):
        base_damage = eval(
            AutoCombatConfig.BASE_DAMAGE_FORMULA,
            {
                'enemy_power': effective_enemy_power,
                'player_defense': self.player.stats['defense']
            }
        )
        min_damage = self.player.max_health * AutoCombatConfig.MINIMUM_DAMAGE_PERCENT
        return max(base_damage, min_damage)
