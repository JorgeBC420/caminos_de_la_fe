class Jewelry:
    def __init__(self, name, stat_modifiers, unique_effect=None):
        self.name = name
        self.stat_modifiers = stat_modifiers  # Dict con modificadores: {'inteligencia': +5}
        self.unique_effect = unique_effect  # Efectos pasivos únicos como regeneración

    def apply_effects(self, player):
        for stat, value in self.stat_modifiers.items():
            player.stats[stat] += value