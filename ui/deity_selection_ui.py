from ursina import *
from data.deity_data import DEITIES

class DeitySelectionUI(Entity):
    def __init__(self, faction, on_select, **kwargs):
        super().__init__(parent=camera.ui, **kwargs)
        self.faction = faction
        self.on_select = on_select
        self.panel = Entity(parent=self, model='quad', scale=(0.8, 0.6), color=color.azure)
        Text(parent=self.panel, text='Elige tu patrón espiritual', y=0.3, scale=1.3)
        for i, deity in enumerate(DEITIES[faction]):
            btn = Button(parent=self.panel, text=f"{deity['name']}\n{deity['passive']}\nUltimate: {deity['ultimate']}", y=0.15-i*0.2, on_click=lambda d=deity: self.select_deity(d))
        Button(parent=self.panel, text='Cerrar', y=-0.25, color=color.red, on_click=self.close)

    def select_deity(self, deity):
        self.on_select(deity)
        destroy(self)

    def close(self):
        destroy(self)
