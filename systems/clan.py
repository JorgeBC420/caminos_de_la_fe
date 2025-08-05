class Clan:
    def __init__(self, name):
        self.name = name
        self.members = []

    def add_member(self, player):
        self.members.append(player)
