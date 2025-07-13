class DailyRewardSystem:
    def __init__(self, player):
        self.player = player
        self.rewards = {
            1: {'gold': 100, 'item': 'small_health_potion'},
            2: {'gold': 200, 'item': None},
            3: {'gold': 300, 'item': 'faction_token'},
        }

    def get_current_streak_day(self):
        return 1

    def update_last_claim(self):
        pass

    def claim_reward(self):
        day = self.get_current_streak_day()
        reward = self.rewards.get(day)
        if reward:
            self.player.gold += reward['gold']
            if reward['item']:
                self.player.inventory.add(reward['item'])
            self.update_last_claim()
            return reward
        return None
