from entities.legendary_item import LegendaryItem

class Inventory:
    def __init__(self):
        self.gold = 0
        self.items = []
        self.equipment = {
            'arma': None,
            'escudo': None,
            'armadura': None,
            'casco': None,
            'botas': None,
            'montura': None,
            'joyeria': None,
            'pocion': None,
        }

    def add_item(self, item):
        self.items.append(item)

    def equip(self, slot, item):
        if slot in self.equipment:
            self.equipment[slot] = item

    def unequip(self, slot):
        if slot in self.equipment:
            self.equipment[slot] = None

    def has_legendary_item(self):
        return any(isinstance(i, LegendaryItem) for i in self.items)
