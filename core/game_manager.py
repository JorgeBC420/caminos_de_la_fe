from scenes.map_scene import MapScene
from scenes.combat_scene import CombatScene
from scenes.profile_scene import ProfileScene

class Game:
    def __init__(self):
        self.current_scene = None
        self.player = None  # Inicializa el jugador

    def start_game(self):
        self.load_map_scene()

    def switch_scene(self, new_scene):
        """Helper function to switch scenes.

        Args:
            new_scene: The new scene to load.
        """
        if self.current_scene:
            self.current_scene.disable()
        self.current_scene = new_scene
        self.current_scene.enable()

    def load_map_scene(self):
        """Load the MapScene."""
        self.switch_scene(MapScene(self))

    def load_combat_scene(self, mission_data):
        """Load the CombatScene with mission data.

        Args:
            mission_data: Data related to the mission.
        """
        self.switch_scene(CombatScene(self, mission_data))

    def load_profile_scene(self):
        """Load the ProfileScene for the player profile."""
        self.switch_scene(ProfileScene(self.player))

    def mission_complete(self, result):
        """Handle mission completion and reward the player.

        Args:
            result: Dictionary containing mission results (experience, loot).
        """
        if not self.player:
            raise ValueError("Player is not initialized.")
        self.player.progression.add_experience(result['experience'])
        self.player.inventory.add_items(result['loot'])
        self.load_map_scene()

    def quit_game(self):
        # Lógica para salir del juego
        pass
