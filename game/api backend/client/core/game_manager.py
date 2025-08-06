from client.core.api_client import APIClient

class GameManager:
    _instance = None

    @staticmethod
    def instance():
        if GameManager._instance is None:
            GameManager._instance = GameManager()
        return GameManager._instance

    def __init__(self):
        self.player = None
        self.current_scene = None
        self.api = APIClient(base_url="http://localhost:8000", auth_token=None)  # Token debe asignarse tras login

    def set_auth_token(self, token):
        self.api.headers['Authorization'] = f'Bearer {token}'

    def get_war_status(self):
        return self.api.get_current_war()

    def submit_faction_power(self, faction, power):
        return self.api.submit_power(faction, power)

    def claim_daily_reward(self):
        return self.api.claim_daily_reward()

    def go_to_map(self):
        from client.scenes.map_scene import MapScene
        self.current_scene = MapScene()
        self.current_scene.enable()

    def go_to_profile(self):
        # TODO: Load ProfileScene
        pass

    def launch_mission(self, mission_data):
        from client.scenes.combat_scene import CombatScene
        self.current_scene.disable() if self.current_scene else None
        self.current_scene = CombatScene(mission_data)
        self.current_scene.enable()

    def mission_complete(self, result):
        # Grant XP and loot to player
        if self.player and hasattr(self.player, 'progression'):
            self.player.progression.add_experience(result.get('xp', 0))
            # TODO: Add loot to inventory
        # Sincronizar recompensa diaria
        daily = self.claim_daily_reward()
        if daily and daily.get('success'):
            print(f"Recompensa diaria: {daily['reward']}")
        # Return to map
        self.current_scene.disable() if self.current_scene else None
        self.go_to_map()
