from ursina import *

class MainNavBar(Entity):
    def __init__(self, ui_manager, **kwargs):
        super().__init__(parent=camera.ui, **kwargs)
        self.ui_manager = ui_manager

        # Contenedor de la barra
        self.bar_bg = Entity(parent=self, model='quad', scale=(1.9, 0.1), y=-0.45, color=color.black66)
        
        # Botones
        Button(parent=self.bar_bg, text='Hogar', scale_x=0.1, on_click=self.ui_manager.show_profile)
        Button(parent=self.bar_bg, text='Ciudadela', scale_x=0.1, x=-0.2, on_click=self.ui_manager.show_citadel)
        Button(parent=self.bar_bg, text='Hermandad', scale_x=0.1, x=0.2, on_click=self.ui_manager.open_brotherhood_panel)
        Button(parent=self.bar_bg, text='Misiones', scale_x=0.1, x=0.4, on_click=self.ui_manager.open_missions_panel)
        # ... añadir resto de botones (PvP, Guerra, Mail, etc.)
