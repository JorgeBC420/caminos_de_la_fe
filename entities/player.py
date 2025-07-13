from ursina import *
from datetime import datetime
from data.factions import FACTIONS
from data.config import GameConfig
from systems.auto_combat import AutoCombatSystem
from systems.faction_war import FactionWarClient

faction_war_client = FactionWarClient("https://tujuego.com/api")

class Player(Entity):
    def __init__(self, faction_name='Cruzados', joystick=None, **kwargs):
        super().__init__(**kwargs)
        # --- Datos RPG ---
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

        # --- Cámara ---
        camera.parent = self
        camera.position = (0, GameConfig.CAMERA_HEIGHT, -GameConfig.CAMERA_DISTANCE)
        camera.rotation_x = -GameConfig.CAMERA_ANGLE

        # --- Habilidades ---
        self.abilities = {
            'basic_attack': {'cooldown': 0.8, 'ready': True},
            'ability1': {'cooldown': 5, 'ready': True},
            'ability2': {'cooldown': 8, 'ready': True},
            'ultimate': {'cooldown': 30, 'ready': True}
        }

        # --- Joystick Virtual ---
        self.joystick = joystick

        # --- Integración con sistemas externos ---
        self.auto_combat = AutoCombatSystem(self)
        self.faction_war_contribution = 0
        self.last_contribution_date = None
        self.auth_token = "example_token"

    # --- Movimiento y combate visual ---
    def update(self):
        direction = Vec3(0,0,0)
        if self.joystick and self.joystick.value.length() > 0:
            direction = Vec3(self.joystick.value.x, 0, self.joystick.value.y).normalized()
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
            if mouse.x > -0.3:
                if self.can_attack:
                    self.attack()

    def attack(self):
        self.can_attack = False
        invoke(setattr, self, 'can_attack', True, delay=0.8)
        self.animate_position(self.position + self.forward * 1, duration=0.1, curve=curve.linear)
        self.animate_position(self.position, duration=0.1, delay=0.1, curve=curve.linear)
        from entities.enemy import Enemy
        for ent in scene.entities[:]:
            if isinstance(ent, Enemy) and distance(self, ent) < self.attack_range:
                print(f"Golpeaste al enemigo! Daño: {self.attack_damage}")
                ent.take_damage(self.attack_damage)

    def take_damage(self, amount):
        self.health -= amount
        if self.health < 0:
            self.health = 0
        print(f"Jugador recibió daño. Vida restante: {self.health}")

    # --- Integración con guerra de facciones ---
    def calculate_war_power(self):
        base_power = self.auto_combat.calculate_player_power()
        loyalty_bonus = 1 + (self.faction_war_contribution * 0.01)
        return base_power * loyalty_bonus

    def participate_in_war(self):
        today = datetime.now().date()
        if self.last_contribution_date == today:
            return {'success': False, 'message': 'Ya contribuiste hoy'}
        power = self.calculate_war_power()
        response = faction_war_client.safe_request('POST', 'submit_power', json={
            'player_id': self.id,
            'faction': self.faction.name,
            'power': power
        })
        if response and response.status_code == 200:
            self.last_contribution_date = today
            self.faction_war_contribution += 1
            return {'success': True, 'power_contributed': power}
        return {'success': False, 'message': 'Error al conectar'}