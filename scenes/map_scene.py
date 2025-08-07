from ursina import Entity, camera
from ui.main_menu_ui import MainMenuUI

class MapScene(Entity):
    def __init__(self, game):
        super().__init__(parent=camera.ui)
        self.game = game
        self.ui = MainMenuUI(game.player)

    def enable(self):
        super().enable()
        self.ui.enable()

    def disable(self):
        super().disable()
        self.ui.disable()
