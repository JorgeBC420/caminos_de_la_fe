class PlayerHome:
    def __init__(self):
        self.level = 1
        self.upgrades = {
            'rest_bonus': 1,
            'storage': 1,
        }
        self.passive_regen_rate = 0.01

    def get_rest_bonus(self):
        return 1.0 + (self.upgrades['rest_bonus'] * 0.05)

    def upgrade(self, upgrade_key, player_inventory):
        cost = self.get_upgrade_cost(upgrade_key)
        if player_inventory.gold >= cost['gold']:
            player_inventory.gold -= cost['gold']
            self.upgrades[upgrade_key] += 1
            print(f"¡Mejoraste '{upgrade_key}' a nivel {self.upgrades[upgrade_key]}!")
        else:
            print("No tienes suficiente oro.")

    def get_upgrade_cost(self, upgrade_key):
        level = self.upgrades[upgrade_key]
        return {'gold': 100 * level, 'resources': 50 * level}
