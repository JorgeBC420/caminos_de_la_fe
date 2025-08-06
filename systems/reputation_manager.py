class ReputationManager:
    def __init__(self, player):
        self.player = player

    def modify_reputation(self, faction, amount):
        self.player.reputation[faction] = self.player.reputation.get(faction, 0) + amount
        print(f'Reputación {faction}: {self.player.reputation[faction]}')

    def get_reputation(self, faction):
        return self.player.reputation.get(faction, 0)
