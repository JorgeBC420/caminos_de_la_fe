from ursina import *

class ClanMenu(Entity):
    def __init__(self, clan):
        super().__init__()
        self.clan = clan
        # Aquí iría la lógica de UI para mostrar miembros, chat, etc.
