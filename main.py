from ursina import *
# CAMBIO: Importamos las escenas que vamos a gestionar
from scenes.faction_selection import FactionSelectionScreen
from scenes.combat_scene import CombatScene
from systems.lang_manager import _, lang_manager
from systems.async_client import AsyncGameClient
from systems.world_manager import WorldManager

class Game:
    def __init__(self):
        self.app = Ursina(
            title="Caminos de la Fe: Cruzada y Conquista",
            borderless=False,
            fullscreen=False,
        )
        self.game_data = {'faction': None}
        # CAMBIO: Añadimos un atributo para saber qué escena está activa
        self.current_scene = None

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