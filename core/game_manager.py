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

    def mission_complete(self, mission_data):
        """Handle mission completion, show rewards, and return to map scene."""
        if not self.player:
            raise ValueError("Player is not initialized.")
        rewards = mission_data.get('rewards', {})
        self.player.progression.add_experience(rewards.get('xp', 0))
        self.player.inventory.add_items(rewards.get('items', []))
        self.player.gold += rewards.get('gold', 0)
        from ui.rewards_ui import RewardsUI
        def continue_to_map():
            self.load_map_scene()
        RewardsUI(rewards, continue_to_map)

    def quit_game(self):
        # Lógica para salir del juego
        pass
