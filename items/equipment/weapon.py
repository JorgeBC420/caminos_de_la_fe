class Weapon:
    def __init__(self, name, damage_bonus=0, crit_chance=0.0, special_effect=None):
        self.name = name
        self.damage_bonus = damage_bonus
        self.crit_chance = crit_chance
        self.special_effect = special_effect  # Puede ser una función o string con efecto especial

    def get_damage_output(self, base_damage):
        return base_damage + self.damage_bonus