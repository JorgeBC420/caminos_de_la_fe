from ursina import Entity, camera, Button
from ui.main_menu_ui import MainMenuUI

class MapScene(Entity):
    def __init__(self, game):
        super().__init__(parent=camera.ui)
        self.game = game
        self.ui = MainMenuUI(game.player)
        self.mission_btn = Button(parent=self, text='Misiones', y=0.3, scale=(0.2,0.1), on_click=self.open_mission_board)

    def open_mission_board(self):
        from ui.mission_board_ui import MissionBoardUI
        MissionBoardUI(self.game)

    def enable(self):
        super().enable()
        self.ui.enable()

    def disable(self):
        super().disable()
        self.ui.disable()
