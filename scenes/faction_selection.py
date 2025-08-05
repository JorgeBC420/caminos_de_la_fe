# Pantalla de selección de facción
# /scenes/faction_selection.py

from ursina import *

class FactionSelectionScreen(Entity):
    def __init__(self, game, **kwargs):
        super().__init__(parent=scene, **kwargs)
        self.game = game # Guardamos la referencia al controlador principal del juego

        Text("Caminos de la Fe: Cruzada y Conquista", scale=3, y=0.3)
        Text("Elige tu facción", scale=2, y=0.15)
        
        Button('Cruzados', color=color.gold, scale=(0.3, 0.1), y=0, on_click=lambda: self.select_faction('Cruzados'))
        Button('Sarracenos', color=color.green, scale=(0.3, 0.1), y=-0.15, on_click=lambda: self.select_faction('Sarracenos'))
        Button('Antiguos', color=color.magenta, scale=(0.3, 0.1), y=-0.3, on_click=lambda: self.select_faction('Antiguos'))

    def select_faction(self, faction_name):
        """Guarda la facción y le dice al controlador del juego que cambie de escena."""
        self.game.game_data['faction'] = faction_name
        print(f"Facción seleccionada: {self.game.game_data['faction']}")
        
        # CAMBIO CLAVE: En lugar de llamar a una función global,
        # le pedimos al controlador del juego que inicie la siguiente escena.
        self.game.start_combat_scene()