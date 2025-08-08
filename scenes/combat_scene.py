# /scenes/combat_scene.py

from ursina import *
from entities.player import Player
from entities.enemy import Enemy
from entities.health_bar import HealthBar
from ui.virtual_joystick import VirtualJoystick
from ui.skill_buttons import create_skill_buttons

class Estado:
    def __init__(self, nombre, duracion, efecto):
        self.nombre = nombre
        self.duracion = duracion
        self.efecto = efecto

# Modificar sistema de daño para incluir resistencias
class CombatScene(Entity):
    def mission_objectives_completed(self):
        """
        Llama a este método cuando los objetivos de la misión se cumplen.
        Notifica al GameManager para otorgar recompensas y volver al MapScene.
        """
        # Ejemplo de resultado de misión (ajusta según tu lógica real)
        result = {
            'experience': self.game.game_data.get('rewards', {}).get('xp', 100),
            'loot': self.game.game_data.get('rewards', {}).get('items', [])
        }
        if hasattr(self.game, 'mission_complete'):
            self.game.mission_complete(result)
        else:
            print("No se pudo notificar la recompensa al GameManager.")
    def __init__(self, game_manager, mission_data, **kwargs):
        super().__init__(parent=scene, **kwargs)
        self.game_manager = game_manager
        self.mission_data = mission_data

        # --- Entorno Básico ---
        theme = self.mission_data.get('theme', 'bosque')
        if theme == 'bosque':
            ground_color = color.hex('#6A9A40')
            ground_texture = 'white_cube'
        elif theme == 'desierto':
            ground_color = color.yellow
            ground_texture = 'white_cube'
        elif theme == 'monasterio':
            ground_color = color.gray
            ground_texture = 'white_cube'
        else:
            ground_color = color.azure
            ground_texture = 'white_cube'
        self.ground = Entity(model='plane', scale=(100, 1, 100), color=ground_color, texture=ground_texture, texture_scale=(100,100), collider='box')

        # --- UI ---
        self.joystick = VirtualJoystick()
        self.skill_buttons = create_skill_buttons()

        # --- Entidades del Juego ---
        self.player = Player(position=(0, 0.5, 0), joystick=self.joystick)

        camera.parent = self.player
        camera.position = (0, 10, -12)
        camera.rotation_x = -30

        # Inicializar objetivos de misión
        self.mission_objectives = self.mission_data.get('objectives', [])
        self.objective_progress = {}
        self.enemies = []
        for obj in self.mission_objectives:
            if obj['type'] == 'defeat' or obj['type'] == 'kill':
                self.objective_progress[obj['target']] = 0
                for i in range(obj['count']):
                    enemy = Enemy(position=(5*i, 0.5, 5*i), target=self.player, owner_scene=self, enemy_id=obj['target'])
                    self.enemies.append(enemy)

        # UI de facción
        Text(text=f"Facción: {getattr(self.game_manager, 'faction', 'Desconocida')}", 
             origin=(-.5, -.5), 
             position=window.top_left + Vec2(0.01, -0.01),
             scale=1.5
        )

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

        # Contador de enemigos derrotados para objetivos de misión
        self.enemies_defeated = 0
        self.mission_objective_count = self.game.game_data.get('objectives', [{}])[0].get('count', 1)

        # Hook para detectar muerte de enemigos (simulado)
        self.enemy1.on_destroy = self.on_enemy_defeated
        self.enemy2.on_destroy = self.on_enemy_defeated

    def on_enemy_defeated(self):
        self.enemies_defeated += 1
        print(f"Enemigos derrotados: {self.enemies_defeated}/{self.mission_objective_count}")
        if self.enemies_defeated >= self.mission_objective_count:
            self.mission_objectives_completed()
    def on_enemy_defeated(self, enemy):
        enemy_id = getattr(enemy, 'enemy_id', 'enemy')
        if enemy_id in self.objective_progress:
            self.objective_progress[enemy_id] += 1
            print(f"Progreso de objetivo: {enemy_id} - {self.objective_progress[enemy_id]}/{self._get_kill_target_count(enemy_id)}")
            self.check_mission_completion()

    def check_mission_completion(self):
        for obj in self.mission_objectives:
            if obj['type'] in ('defeat', 'kill'):
                if self.objective_progress.get(obj['target'], 0) < obj['count']:
                    return
        print("¡Objetivos de la misión completados!")
        self.game_manager.mission_complete(self.mission_data)

    def _get_kill_target_count(self, target_id):
        for obj in self.mission_objectives:
            if obj['type'] in ('defeat', 'kill') and obj['target'] == target_id:
                return obj['count']
        return 0

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

    def calcular_daño(self, atacante, defensor, habilidad):
        daño_base = atacante.ataque * habilidad.modificador
        resistencia = defensor.resistencias.get(habilidad.tipo, 1.0)
        return max(1, int(daño_base * resistencia))