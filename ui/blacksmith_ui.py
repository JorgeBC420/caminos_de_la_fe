from ursina import *

class BlacksmithUI(Entity):
    def __init__(self, player, **kwargs):
        super().__init__(parent=camera.ui, **kwargs)
        self.player = player
        self.panel = Entity(parent=self, model='quad', scale=(1,0.8), color=color.brown)
        Text(parent=self.panel, text='Herrería', y=0.35, scale=2)
        y = 0.15
        Button(parent=self.panel, text='Forjar Nuevo Equipo', y=y, on_click=self.forge_item)
        y -= 0.12
        Button(parent=self.panel, text='Mejorar Equipo', y=y, on_click=self.upgrade_item)
        Button(parent=self.panel, text='Cerrar', y=-0.35, color=color.red, on_click=self.close)

    def forge_item(self):
        print('Forjar equipo (mock): requiere materiales y oro')

    def upgrade_item(self):
        print('Mejorar equipo (mock): requiere materiales y oro')

    def close(self):
        destroy(self)
