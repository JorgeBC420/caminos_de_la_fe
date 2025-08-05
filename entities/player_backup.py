from ursina import *
from data.factions import FACTIONS
from data.config import GameConfig

class Player(Entity):
    # Modificar el constructor para aceptar el joystick
    def __init__(self, faction_name='Cruzados', joystick=None, **kwargs):
        super().__init__(**kwargs)
        self.faction = FACTIONS[faction_name]
        self.model = 'cube'
        self.color = self.faction.color
        self.collider = 'box'
        self.speed = GameConfig.PLAYER_SPEED
        self.health = GameConfig.PLAYER_HEALTH
        self.max_health = GameConfig.PLAYER_HEALTH
        self.attack_damage = 15
        self.attack_range = 2.5
        self.can_attack = True

        camera.parent = self
        camera.position = (0, GameConfig.CAMERA_HEIGHT, -GameConfig.CAMERA_DISTANCE)
        camera.rotation_x = -GameConfig.CAMERA_ANGLE

        self.abilities = {
            'basic_attack': {'cooldown': 0.8, 'ready': True},
            'ability1': {'cooldown': 5, 'ready': True},
            'ability2': {'cooldown': 8, 'ready': True},
            'ultimate': {'cooldown': 30, 'ready': True}
        }

        # Guardar la referencia al joystick
        self.joystick = joystick

    def update(self):
        direction = Vec3(0,0,0) # Vector de dirección inicial

        # --- Lógica de Movimiento Flexible ---
        # Prioridad 1: Joystick Virtual
        if self.joystick and self.joystick.value.length() > 0:
            direction = Vec3(self.joystick.value.x, 0, self.joystick.value.y).normalized()
        # Prioridad 2: Teclas WASD
        else:
            direction = Vec3(
                held_keys['d'] - held_keys['a'],
                0,
                held_keys['w'] - held_keys['s']
            ).normalized()
        
        self.position += direction * self.speed * time.dt

        if direction.length() > 0:
            self.look_at(self + direction, axis='y')

    def input(self, key):
        if key == 'left mouse down':
            # Evitamos que el clic del joystick dispare un ataque
            if mouse.x > -0.3: # Si el ratón no está en la zona del joystick
                if self.can_attack:
                    self.attack()

    def attack(self):
        self.can_attack = False
        invoke(setattr, self, 'can_attack', True, delay=0.8)

        self.animate_position(self.position + self.forward * 1, duration=0.1, curve=curve.linear)
        self.animate_position(self.position, duration=0.1, delay=0.1, curve=curve.linear)

        from entities.enemy import Enemy # Importación local para evitar importación circular
        for ent in scene.entities[:]:
            if isinstance(ent, Enemy) and distance(self, ent) < self.attack_range:
                print(f"Golpeaste al enemigo! Daño: {self.attack_damage}")
                ent.take_damage(self.attack_damage)
                
    def take_damage(self, amount):
        self.health -= amount
        if self.health < 0:
            self.health = 0
        print(f"Jugador recibió daño. Vida restante: {self.health}")