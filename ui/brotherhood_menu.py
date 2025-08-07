# Migración desde clan_menu.py

class BrotherhoodMenu(Entity):
    def __init__(self, brotherhood):
        super().__init__()
        self.brotherhood = brotherhood

    def display_menu(self):
        print(f"Menú de la hermandad: {self.brotherhood.name}")
