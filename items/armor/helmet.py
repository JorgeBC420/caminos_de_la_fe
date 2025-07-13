class Helmet:
    def __init__(self, name, defense, resistance, weight='medio'):
        self.name = name
        self.defense = defense
        self.resistance = resistance
        self.weight = weight

    def apply_effects(self, player_stats):
        player_stats['defensa'] += self.defense
        player_stats['resistencia'] += self.resistance
        if self.weight == 'pesado':
            player_stats['agilidad'] -= 1