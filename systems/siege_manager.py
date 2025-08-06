class SiegeManager:
    def __init__(self, player):
        self.player = player
        self.units = []
        self.defenses = []

    def recruit_unit(self, unit):
        self.units.append(unit)

    def place_defense(self, defense):
        self.defenses.append(defense)
