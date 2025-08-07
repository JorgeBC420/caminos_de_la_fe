
from ursina import *

# CAMBIO: Importamos las escenas que vamos a gestionar
from scenes.faction_selection import FactionSelectionScreen
from scenes.combat_scene import CombatScene
from scenes.profile_scene import ProfileScene
from systems.lang_manager import _, lang_manager
from systems.async_client import AsyncGameClient
from systems.world_manager import WorldManager
from quests.quest import Quest
from ui.deity_selection_ui import DeitySelectionUI
from systems.reputation_manager import ReputationManager
from scenes.siege_scene import SiegeScene
from core.ui_manager import UIManager
import json
from ui.profile_ui import ProfileUI
from ui.event_end_ui import EventEndUI
# Ejemplo: cómo disparar la conversión desde la UI al finalizar un evento
def finalizar_evento_y_convertir(player, event_name):
    EventEndUI(player, event_name)

class Game:

    def __init__(self):
        import data.config as config
        from quests.quest import Quest
        self.app = Ursina(
            title=_("Paths of Faith: Crusade and Conquest"),
            borderless=False,
            fullscreen=False,
        )
        self.ui_manager = UIManager(game_manager=self, player=None)
        self.background_entity = None
        self.player_entity = None
        self.current_section = 'home'
        self.section_backgrounds = {
            'home': 'assets/home/home.png',
            'ciudadela': 'assets/ciudadela/ciudadela.png',
            'hermandad': 'assets/fortaleza/fortaleza.png',
            'pvp_guerrahermandades': 'assets/guerrahermandades/guerrahermandades.png',
            'pvp_guerradelafe': 'assets/guerradelafe/guerradelafe.png',
            'misiones': 'assets/missions/missions.png',
        }

        # Barra de navegación inferior
        self.nav_buttons = []
        nav_data = [
            ("Perfil", self.on_home_click),
            ("Ciudadela", self.on_ciudadela_click),
            ("Hermandad", self.on_hermandad_click),
            ("PvP Hermandades", self.on_pvp_guerrahermandades_click),
            ("PvP Fe", self.on_pvp_guerradelafe_click),
            ("Misiones", self.on_misiones_click),
        ]
        for i, (label, callback) in enumerate(nav_data):
            btn = Button(
                text=label,
                parent=camera.ui,
                scale=(0.18, 0.07),
                position=(-0.7 + i*0.28, -0.48),
                color=color.dark_gray,
                highlight_color=color.azure,
                pressed_color=color.orange,
                on_click=callback
            )
            self.nav_buttons.append(btn)

    def show_section(self, section):
        """Cambia el fondo y muestra el modelo del jugador en modo idle."""
        self.current_section = section
        # Eliminar fondo anterior
        if self.background_entity:
            destroy(self.background_entity)
        # Cargar nuevo fondo
        bg_path = self.section_backgrounds.get(section, 'assets/home/home.png')
        self.background_entity = Entity(
            parent=camera.ui,
            model='quad',
            texture=bg_path,
            scale=(2, 1.2),
            z=1
        )
        # Eliminar modelo anterior del jugador
        if self.player_entity:
            destroy(self.player_entity)
        # Cargar modelo poligonal del jugador en modo idle (ejemplo: Soldado CRUZADO.fbx)
        # Aquí puedes personalizar según la clase/facción del jugador
        player_model = getattr(self, 'player', None)
        model_path = 'Soldado CRUZADO.fbx' if not player_model else player_model.model_path
        self.player_entity = Entity(
            parent=camera.ui,
            model=model_path,
            scale=0.12,
            position=(0, -0.25, -0.5),
            rotation=(0, 180, 0),
            z=0.5
        )
        # Aquí puedes añadir animación idle si el modelo lo soporta

    # Métodos para los botones inferiores
    def on_home_click(self):
        self.show_section('home')

    def on_ciudadela_click(self):
        self.show_section('ciudadela')

    def on_hermandad_click(self):
        self.show_section('hermandad')

    def on_pvp_guerrahermandades_click(self):
        self.show_section('pvp_guerrahermandades')

    def on_pvp_guerradelafe_click(self):
        self.show_section('pvp_guerradelafe')

    def on_misiones_click(self):
        self.show_section('misiones')

    def assign_initial_quest(self):
        # Actualización de la misión inicial para el tutorial
        self.active_quest = Quest(
            "Tutorial: Primeros Pasos",
            "Aprende los conceptos básicos del juego",
            {"collect": 1, "interact": 1},
            "General",
            {"xp": 50, "gold": 10}
        )

    def assign_fragment_quest(self):
        # Agregar misión de fragmentos de armas legendarias
        self.active_quest = Quest(
            "Fragmentos Perdidos",
            "Recolecta fragmentos de armas legendarias",
            {"collect": 3, "explore": 2},
            "General",
            {"xp": 300, "gold": 100}
        )

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
        
        # Ejemplo de uso del UIManager
        self.ui_manager.show_profile()

    # CAMBIO: Añadimos el método para iniciar la escena de combate
    def start_combat_scene(self):
        print("Iniciando escena de combate...")
        # Aquí iría la lógica para iniciar la escena de combate

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

selected_faction = None
selected_deity = None
player = None
reputation_manager = None

def select_faction(faction_name):
    global selected_faction, selection_menu_items
    selected_faction = faction_name
    print(f"Faccion seleccionada: {selected_faction}")
    for item in selection_menu_items:
        item.disable()
    # Selección de deidad tras elegir facción
    DeitySelectionUI(faction_name, on_select=select_deity)

def select_deity(deity):
    global selected_deity, player, reputation_manager
    selected_deity = deity
    print(f"Deidad seleccionada: {deity['name']}")
    # Inicializa reputación y jugador
    reputation_manager = ReputationManager(player)
    player.deity = deity
    player.passive = deity['passive']
    player.ultimate = deity['ultimate']
    player.ultimate_desc = deity['ultimate_desc']
    player.moral = 0  # Moral/fe inicial
    # Llama a la escena de combate desde la instancia de Game si está disponible
    if 'game' in globals() and hasattr(game, 'start_combat_scene'):
        game.start_combat_scene()
    else:
        print("No se pudo iniciar la escena de combate: instancia de Game no encontrada.")

# Ejemplo de uso
if __name__ == "__main__":
    game = Game()
    game.run()

# En la UI de combate, solo permite activar ultimate si player.moral >= 500
# Ejemplo de lógica para el botón de ultimate:

# --- Eliminar duplicados y funciones sueltas ---