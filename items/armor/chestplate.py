class Chestplate:
    def __init__(self, name, defense, resistance, penalties=None):
        self.name = name
        self.defense = defense
        self.resistance = resistance
        self.penalties = penalties or {'velocidad': -1, 'agilidad': -1}

    def apply_effects(self, player_stats):
        player_stats['defensa'] += self.defense
        player_stats['resistencia'] += self.resistance
        for stat, value in self.penalties.items():
            player_stats[stat] += value