from ursina import *
from scenes.profile_scene import ProfileScene
from scenes.citadel_scene import CitadelScene
from ui.brotherhood_ui import BrotherhoodUI
from ui.mission_ui import MissionUI
# ... importar todas las demás clases de UI

class UIManager:
    def __init__(self, game_manager, player):
        self.game_manager = game_manager
        self.player = player
        
        self.active_base_scene = None
        self.active_panel = None

    def show_profile(self):
        """Muestra la escena de perfil como base."""
        self._clear_base_scene()
        self.active_base_scene = ProfileScene(player=self.player, game_manager=self.game_manager)

    def show_citadel(self):
        """Muestra la escena de la ciudadela como base."""
        self._clear_base_scene()
        self.active_base_scene = CitadelScene(player=self.player, game_manager=self.game_manager)

    def open_brotherhood_panel(self):
        self._open_panel(BrotherhoodUI)

    def open_missions_panel(self):
        self._open_panel(MissionUI)

    def _open_panel(self, PanelClass):
        """Función genérica para abrir un panel modal."""
        if self.active_panel:
            destroy(self.active_panel)
        
        self.active_panel = PanelClass(player=self.player, ui_manager=self)
        
    def _clear_base_scene(self):
        if self.active_base_scene:
            destroy(self.active_base_scene)
