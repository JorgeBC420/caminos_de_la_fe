class Shield:
    def __init__(self, name, block_chance, defense_bonus):
        self.name = name
        self.block_chance = block_chance  # porcentaje de bloqueo
        self.defense_bonus = defense_bonus

    def apply_effects(self, player_stats):
        player_stats['defensa'] += self.defense_bonus