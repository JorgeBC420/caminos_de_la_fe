class ReputationSystem:
    def __init__(self, player):
        self.player = player
        self.reputation = {'Cruzados': 0, 'Sarracenos': 0, 'Antiguos': 0}

    def adjust_reputation(self, faction, amount):
        self.reputation[faction] += amount
