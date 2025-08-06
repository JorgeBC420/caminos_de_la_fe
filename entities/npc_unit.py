class NPCUnit:
    def __init__(self, name, faction, stats=None):
        self.name = name
        self.faction = faction
        self.stats = stats or {}
        self.ai_controlled = True
