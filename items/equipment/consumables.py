class Consumable:
    def __init__(self, name, effect, uses=1):
        self.name = name
        self.effect = effect  # Función o string que describe el efecto
        self.uses = uses

    def use(self, target):
        if self.uses > 0:
            self.effect(target)
            self.uses -= 1