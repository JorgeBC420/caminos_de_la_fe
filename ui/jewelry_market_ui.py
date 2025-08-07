from ursina import *

class JewelryMarketUI(Entity):
    def __init__(self, player, **kwargs):
        super().__init__(parent=camera.ui, **kwargs)
        self.player = player
        self.panel = Entity(parent=self, model='quad', scale=(0.8, 0.7), color=color.yellow.tint(-.2))
        Text(parent=self.panel, text='Mercado de Joyas/Items (P2P)', y=0.3, scale=1.5)
        Button(parent=self.panel, text='Cerrar', y=-0.4, color=color.red, on_click=self.close)

    def close(self):
        destroy(self)
