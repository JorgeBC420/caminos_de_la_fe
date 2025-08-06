from ursina import *

class HomeUI(Entity):
    def __init__(self, player_home, player_inventory, **kwargs):
        super().__init__(parent=camera.ui, **kwargs)
        self.home = player_home
        self.inventory = player_inventory
        self.panel = Entity(parent=self, model='quad', scale=(0.8, 0.6), color=color.dark_gray)
        Text(parent=self.panel, text="Mi Ciudadela", y=0.4)
        cost = self.home.get_upgrade_cost('rest_bonus')
        self.rest_btn = Button(
            parent=self.panel,
            text=f"Mejorar Descanso (Nivel {self.home.upgrades['rest_bonus']}) \nCosto: {cost['gold']} Oro",
            y=0.1, color=color.azure,
            on_click=lambda: self.home.upgrade('rest_bonus', self.inventory)
        )
        Button(parent=self.panel, text="Cerrar", y=-0.4, on_click=destroy, target=self)
