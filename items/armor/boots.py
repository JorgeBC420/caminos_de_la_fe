class Boots:
    def __init__(self, name, bonuses, weight='ligero'):
        self.name = name
        self.bonuses = bonuses  # {'velocidad': 3, 'agilidad': 2, 'destreza': 1}
        self.weight = weight  # 'ligero', 'medio', 'pesado'

    def apply_effects(self, player_stats):
        for stat, value in self.bonuses.items():
            player_stats[stat] += value