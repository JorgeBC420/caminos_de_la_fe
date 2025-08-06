from ursina import *

class MainMapUI(Entity):
    def __init__(self, player, **kwargs):
        super().__init__(parent=camera.ui, **kwargs)
        self.player = player
        self.panel = Entity(parent=self, model='quad', scale=(1.5, 1.0), color=color.green.tint(-0.3))
        Text(parent=self.panel, text='Mapa Principal', y=0.4, scale=1.5)
        # Nodos de misiones
        self.mission_node = Button(parent=self.panel, text='Misiones', position=(-0.5,0.2), color=color.gold, scale=(0.18,0.18))
        # Nodos de eventos
        self.event_node = Button(parent=self.panel, text='Eventos', position=(0.0,0.2), color=color.magenta, scale=(0.18,0.18))
        # Nodos de fortalezas
        self.siege_node = Button(parent=self.panel, text='Fortalezas', position=(0.5,0.2), color=color.azure, scale=(0.18,0.18))
        # Accesos rápidos
        self.hero_btn = Button(parent=self.panel, text='Héroe', position=(-0.6,-0.3), scale=(0.14,0.14))
        self.clan_btn = Button(parent=self.panel, text='Clanes', position=(0.0,-0.3), scale=(0.14,0.14))
        self.event_btn = Button(parent=self.panel, text='Eventos', position=(0.6,-0.3), scale=(0.14,0.14))
        self.siege_btn = Button(parent=self.panel, text='Asedio', position=(0.3,-0.3), scale=(0.14,0.14))
