# Migración desde clan.py

class Brotherhood:
    def __init__(self, name, members):
        self.name = name
        self.members = members

    def add_member(self, member):
        self.members.append(member)

    def remove_member(self, member):
        self.members.remove(member)

    def declare_war(self, other_brotherhood):
        print(f"{self.name} declara la guerra a {other_brotherhood.name}")
