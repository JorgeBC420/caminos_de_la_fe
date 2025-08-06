from ursina import *
from data.deity_data import DEITIES

class HeroMenuUI(Entity):
    def __init__(self, player, **kwargs):
        super().__init__(parent=camera.ui, **kwargs)
        self.player = player
        self.panel = Entity(parent=self, model='quad', scale=(1.0, 0.8), color=color.azure)
        Text(parent=self.panel, text='Menú de Héroe', y=0.3, scale=1.3)
        # Pestañas para habilidades, equipamiento, deidad y recursos
        self._draw_deity_section()

    def _draw_deity_section(self):
        if hasattr(self.player, 'deity') and self.player.deity:
            d = self.player.deity
            Text(parent=self.panel, text=f'Deidad: {d["name"]}', y=0.15, scale=1.1)
            Text(parent=self.panel, text=f'Pasivo: {d["passive"]}', y=0.08, scale=1)
            Text(parent=self.panel, text=f'Ultimate: {d["ultimate"]}', y=0.0, scale=1)
            Text(parent=self.panel, text=f'{d["ultimate_desc"]}', y=-0.07, scale=0.9)
        else:
            Text(parent=self.panel, text='Sin deidad seleccionada', y=0.1, scale=1)
