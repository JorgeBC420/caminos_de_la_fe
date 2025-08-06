class WorldManager:
    WORLDS = {
        "holy_land": {"name": "Tierra Santa", "factions": ["Antiguos", "Sarracenos", "Cruzados"]},
        "expansion1": {"name": "Reinos del Nilo", "factions": ["Egipcios", "Romanos"]},
        "expansion2": {"name": "Tierras Boreales", "factions": ["Vikingos", "Griegos"]},
    }
    def __init__(self):
        self.current_world = "holy_land"
        self.player_worlds = {}
    def get_available_worlds(self):
        return list(self.WORLDS.keys())
    def switch_world(self, world_id, player_data):
        if world_id not in self.WORLDS:
            return False
        self.save_player_state(player_data)
        self.current_world = world_id
        self.load_world_environment(world_id)
        return True
    def save_player_state(self, player_data):
        self.player_worlds[self.current_world] = player_data
    def load_world_environment(self, world_id):
        world_data = self.WORLDS[world_id]
        print(f"Cargando mundo: {world_data['name']}")
        # Aquí se cargarían los assets específicos del mundo
