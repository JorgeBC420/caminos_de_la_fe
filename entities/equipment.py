class Equipment:
    def __init__(self):
        self.arma = None
        self.escudo = None
        self.armadura = None
        self.casco = None
        self.botas = None
        self.montura = None
        self.joyeria = None
        self.pocion = None

    def equip(self, slot, item):
        if hasattr(self, slot):
            setattr(self, slot, item)

    def unequip(self, slot):
        if hasattr(self, slot):
            setattr(self, slot, None)
