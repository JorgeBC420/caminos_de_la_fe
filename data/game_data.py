class GameData:
    def __init__(self):
        self.faction = None
        self.level = 1
        self.xp = 0
        self.gold = 0
        self.resources = {}
        self.abilities = []
        self.ultimate = None
        self.inventory = []
        self.mission_progress = {}
        self.side_quest_progress = {}
        self.city_state = {}
        self.state = {}
        self.progress = {}

    def set_faction(self, faction):
        self.faction = faction

    def unlock_ability(self, ability):
        if ability not in self.abilities:
            self.abilities.append(ability)

    def set_ultimate(self, ultimate):
        self.ultimate = ultimate

    def add_item(self, item):
        self.inventory.append(item)

    def remove_item(self, item):
        if item in self.inventory:
            self.inventory.remove(item)

    def update_mission(self, mission_id, status):
        self.mission_progress[mission_id] = status

    def update_side_quest(self, quest_id, status):
        self.side_quest_progress[quest_id] = status

    def add_resource(self, resource, amount):
        self.resources[resource] = self.resources.get(resource, 0) + amount

    def spend_resource(self, resource, amount):
        if self.resources.get(resource, 0) >= amount:
            self.resources[resource] -= amount
            return True
        return False

    def save(self, filename):
        import json
        data = self.__dict__.copy()
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def load(self, filename):
        import json
        with open(filename, 'r', encoding='utf-8') as f:
            data = json.load(f)
        self.__dict__.update(data)
