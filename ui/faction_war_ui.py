from ursina import *
from systems.faction_war import FactionWarClient

class FactionWarUI(Entity):
    def __init__(self, player, **kwargs):
        super().__init__(parent=camera.ui, **kwargs)
        self.player = player
        self.client = FactionWarClient("https://tujuego.com/api", auth_token=player.auth_token)
        self.status_text = None
        self.progress_bars = {}
        self.contribute_button = None
        self.rewards_button = None
        self.create_ui()
        self.update_ui()

    def create_ui(self):
        Entity(parent=self, model='quad', scale=(0.8, 0.3), color=color.black66)
        self.status_text = Text(parent=self, position=(-0.35, 0.1))
        self.progress_bars['Cruzados'] = Entity(parent=self, model='quad', color=color.gold, position=(-0.35, 0), scale=(0, 0.05))
        self.progress_bars['Sarracenos'] = Entity(parent=self, model='quad', color=color.green, position=(0.35, 0), scale=(0, 0.05))
        self.contribute_button = Button(parent=self, text='Contribuir', position=(0, -0.1), scale=(0.2, 0.05), on_click=self.on_contribute)
        self.rewards_button = Button(parent=self, text='Recompensas', position=(0.2, -0.1), scale=(0.2, 0.05), on_click=self.show_rewards)

    def update_ui(self):
        pass

    def on_contribute(self):
        if self.player.participate_in_war().get('success'):
            self.contribute_button.text = "¡Contribuido!"
            self.contribute_button.color = color.azure
            invoke(setattr, self.contribute_button, 'text', 'Contribuir', delay=3)
            invoke(setattr, self.contribute_button, 'color', color.white, delay=3)

    def show_rewards(self):
        print("Mostrar recompensas")
