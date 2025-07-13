# /scenes/combat_scene.py

from ursina import *
from entities.player import Player
from entities.enemy import Enemy
from entities.health_bar import HealthBar
from ui.virtual_joystick import VirtualJoystick
from ui.skill_buttons import create_skill_buttons

class CombatScene(Entity):
    def __init__(self, game, **kwargs):
        super().__init__(parent=scene, **kwargs)
        self.game = game # Guardamos una referencia al controlador principal del juego

        # --- Entorno Básico ---
        self.ground = Entity(model='plane', scale=(100, 1, 100), color=color.hex('#6A9A40'), texture='white_cube', texture_scale=(100,100), collider='box')
        
        # --- UI ---
        # Primero creamos los elementos de UI para que estén listos
        self.joystick = VirtualJoystick()
        self.skill_buttons = create_skill_buttons()

        # --- Entidades del Juego ---
        # Pasamos el joystick recién creado al jugador en su constructor
        self.player = Player(position=(0, 0.5, 0), joystick=self.joystick)
        
        # Le decimos a la cámara que siga al jugador (podría estar en la clase Player también)
        camera.parent = self.player
        camera.position = (0, 10, -12)
        camera.rotation_x = -30
        
        # Crear enemigos que apunten al jugador
        self.enemy1 = Enemy(position=(10, 0.5, 5), target=self.player)
        self.enemy2 = Enemy(position=(-5, 0.5, 10), target=self.player)

        # --- UI Vinculada a Entidades ---
        # Barra de vida del jugador
        self.player_hp_bar = HealthBar(
            max_value=self.player.max_health,
            position=window.bottom_left + Vec2(0.38, 0.07),
            scale=(0.5, 0.04) # Un poco más grande
        )
        self.player_hp_bar.bind_to_attribute(self.player, 'health', 'value')
        
        # Pequeño texto para mostrar la facción elegida
        Text(text=f"Facción: {self.game.game_data['faction']}", 
             origin=(-.5, -.5), 
             position=window.top_left + Vec2(0.01, -0.01),
             scale=1.5
        )

    # Puedes añadir aquí métodos para gestionar la escena, como pausar, terminar, etc.
    # Por ejemplo, un método para limpiar la escena cuando el jugador muere.
    def cleanup(self):
        print("Limpiando la escena de combate...")
        # Destruir todas las entidades creadas en esta escena
        destroy(self.ground)
        destroy(self.player)
        destroy(self.enemy1)
        destroy(self.enemy2)
        destroy(self.joystick)
        destroy(self.player_hp_bar)
        for btn in self.skill_buttons.values():
            destroy(btn)
        # Finalmente, destruir la propia escena
        destroy(self)