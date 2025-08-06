from ursina import *

class MapScene(Entity):
    def __init__(self):
        super().__init__()
        self.profile_button = Button(text='Perfil', position=(-0.5,0.4), scale=(0.2,0.1), on_click=self.open_profile)
        self.brotherhood_button = Button(text='Hermandad', position=(-0.5,0.2), scale=(0.2,0.1), on_click=self.open_brotherhood)
        self.home_button = Button(text='Hogar', position=(-0.5,0.0), scale=(0.2,0.1), on_click=self.open_home)
        self.mission_board_button = Button(text='Tablón de Misiones', position=(-0.5,-0.2), scale=(0.2,0.1), on_click=self.open_mission_board)

    def open_profile(self):
        from client.core.game_manager import GameManager
        GameManager.instance().go_to_profile()

    def open_brotherhood(self):
        # TODO: Open Brotherhood UI
        pass

    def open_home(self):
        # TODO: Open Home UI
        pass

    def open_mission_board(self):
        from client.ui.mission_selection_ui import MissionSelectionUI
        MissionSelectionUI().enable()
