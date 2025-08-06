from ursina import *

class CombatHUD(Entity):
    def __init__(self, player, **kwargs):
        super().__init__(parent=camera.ui, **kwargs)
        self.player = player
        self.panel = Entity(parent=self, model='quad', scale=(1.2, 0.3), color=color.black33)
        # Botón de ataque básico
        self.attack_btn = Button(parent=self.panel, text='Atacar', position=(-0.4, 0), scale=(0.18,0.18))
        # Botón de habilidad 1
        self.skill1_btn = Button(parent=self.panel, text='Habilidad 1', position=(0.0, 0), scale=(0.16,0.16))
        # Botón de habilidad 2
        self.skill2_btn = Button(parent=self.panel, text='Habilidad 2', position=(0.2, 0), scale=(0.16,0.16))
        # Botón de ultimate
        self.ultimate_btn = Button(parent=self.panel, text='Ultimate', position=(0.4, 0), scale=(0.18,0.18), color=color.yellow.tint(-0.2))
        # Botón de evadir
        self.evade_btn = Button(parent=self.panel, text='Evadir', position=(-0.6, 0), scale=(0.14,0.14), color=color.azure)
        # Barra de salud
        self.health_bar = Entity(parent=self.panel, model='quad', color=color.red, scale=(0.7,0.05), position=(0,0.18))
        # Minimap (placeholder)
        self.minimap = Entity(parent=self.panel, model='circle', color=color.green.tint(-0.5), scale=(0.12,0.12), position=(0.6,0.18))
