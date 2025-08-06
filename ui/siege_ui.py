from ursina import *

class SiegeUI(Entity):
    def __init__(self, siege_manager, **kwargs):
        super().__init__(parent=camera.ui, **kwargs)
        self.siege_manager = siege_manager
        self.panel = Entity(parent=self, model='quad', scale=(1.0, 0.7), color=color.gray)
        Text(parent=self.panel, text='Gestión de Asedio', y=0.3, scale=1.2)
        # Aquí iría la UI para reclutar y gestionar unidades y defensas
