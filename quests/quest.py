class Quest:
    def __init__(self, title, description, objectives, faction, rewards):
        self.title = title
        self.description = description
        self.objectives = objectives  # dict: {'collect': 5, 'kill_enemies': 3}
        self.faction = faction
        self.rewards = rewards  # dict: {'xp': 200, 'gold': 50}
        self.completed = False
        self.progress = {key: 0 for key in objectives}

    def update_progress(self, key, amount=1):
        if key in self.progress:
            self.progress[key] += amount
            if self.progress[key] >= self.objectives[key]:
                self.progress[key] = self.objectives[key]
        self.check_completion()

    def check_completion(self):
        self.completed = all(self.progress[k] >= self.objectives[k] for k in self.objectives)
        return self.completed

    def claim_rewards(self, player):
        if self.completed:
            player.add_xp(self.rewards.get('xp', 0))
            player.gold += self.rewards.get('gold', 0)
            # Aquí puedes agregar más tipos de recompensas
            return True
        return False
