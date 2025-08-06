class Unit:
    def __init__(self, name, unit_type, stats=None):
        self.name = name
        self.unit_type = unit_type
        self.stats = stats or {}
        self.ai_controlled = True
