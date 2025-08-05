from ursina import *
# CAMBIO: Importamos las escenas que vamos a gestionar
from scenes.faction_selection import FactionSelectionScreen
from scenes.combat_scene import CombatScene
from scenes.profile_scene import ProfileScene
from systems.lang_manager import _, lang_manager
from systems.async_client import AsyncGameClient
from systems.world_manager import WorldManager
from quests.quest import Quest
import json

class Game:

    def __init__(self):
        import data.config as config
        from quests.quest import Quest
        self.app = Ursina(
            title="Caminos de la Fe: Cruzada y Conquista",
            borderless=False,
            fullscreen=False,
        )
        self.game_data = {'faction': None}
        self.current_scene = None
        self.game_state = 'menu'
        self.valid_states = config.GameConfig.GAME_STATES
        self.active_quest = None

    def assign_initial_quest(self):
        if self.game_data['faction'] == 'Cruzados':
            self.active_quest = Quest(
                "La Plaga de los Susurros",
                "Recolecta lágrimas de fénix",
                {"collect": 5, "kill_enemies": 3},
                "Cruzados",
                {"xp": 200, "gold": 50}
            )
        # Puedes agregar más lógica para otras facciones

    def set_game_state(self, state):
        if state in self.valid_states:
            self.game_state = state
        else:
            print(f"Estado de juego inválido: {state}")

    def is_state(self, state):
        return self.game_state == state

    def run(self):
        # Iniciar con la pantalla de selección de facción
        self.start_faction_selection()
        self.app.run()

    def start_faction_selection(self):
        """Inicia la pantalla de selección de facción."""
        print("Iniciando selección de facción...")
        
        # Si ya había una escena antes (ej: volver al menú), la limpiamos
        if self.current_scene and hasattr(self.current_scene, 'cleanup'):
            self.current_scene.cleanup()
        
        window.color = color.dark_gray
        # Creamos una instancia de FactionSelectionScreen y la guardamos
        self.current_scene = FactionSelectionScreen(game=self)

    # CAMBIO: Añadimos el método para iniciar la escena de combate
    def start_combat_scene(self):
        """Limpia la escena actual e inicia la escena de combate."""
        print("Iniciando escena de combate...")
        
        # La escena de selección de facción limpia sus propios botones al hacer clic.
        # Nos aseguramos de limpiar cualquier remanente por si acaso.
        for entity in scene.entities:
            if isinstance(entity, (Button, Text)):
                destroy(entity)

        window.color = color.hex('#82C5FF')
        # Creamos una instancia de CombatScene y la guardamos
        self.current_scene = CombatScene(game=self)

    def save_game(self):
        player_data = self.current_scene.player.save_state()
        with open('save_game.json', 'w') as f:
            json.dump(player_data, f, indent=4)
        print("¡Juego guardado!")

    def load_game(self):
        try:
            with open('save_game.json', 'r') as f:
                player_data = json.load(f)
            self.start_combat_scene()
            self.current_scene.player.load_state(player_data)
            print("¡Juego cargado!")
        except FileNotFoundError:
            print("No se encontró un archivo de guardado.")

    def open_profile(self, player):
        # Limpiar escena actual
        for entity in scene.entities:
            if entity not in [camera, camera.ui]:
                destroy(entity)
        # Crear nueva escena de perfil
        profile_scene = ProfileScene(player)
        profile_ui = ProfileUI(player)

class GameWorld(Entity):
    def __init__(self, world_id):
        super().__init__()
        self.world_id = world_id
        self.async_client = AsyncGameClient()
        self.world_manager = WorldManager()
        self.player_data = {
            "id": "player123",
            "faction": "Cruzados",
            "stats": {"fuerza": 10, "defensa": 8},
            "equipment": {"arma": "Espada", "armadura": "Cota"}
        }
    def join_holy_war(self):
        self.async_client.join_holy_war(
            war_id="holy_war_2023",
            player_data=self.player_data,
            callback=self.on_war_result
        )
    def on_war_result(self, result):
        print(_("war_result_message"))
        self.show_battle_cinematic(result)
    def show_battle_cinematic(self, result):
        if result.get("victory", False):
            print("Animación de victoria")
        else:
            print("Animación de derrota")
    def switch_world(self, world_id):
        self.world_manager.switch_world(world_id, self.player_data)

# Ejemplo de uso
if __name__ == "__main__":
    app = Ursina()
    game = GameWorld(world_id="holy_land")
    game.join_holy_war()
    game.switch_world("europe")
    app.run()