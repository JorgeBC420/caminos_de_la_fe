# Clase Player
from ursina import *
from data.factions import FACTIONS
from data.config import GameConfig

class Player(Entity):
    def __init__(self, faction_name='Cruzados', **kwargs):
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

        camera.parent = self
        camera.position = (0, GameConfig.CAMERA_HEIGHT, -GameConfig.CAMERA_DISTANCE)
        camera.rotation_x = -GameConfig.CAMERA_ANGLE

        self.abilities = {
            'basic_attack': {'cooldown': 0.8, 'ready': True},
            'ability1': {'cooldown': 5, 'ready': True},
            'ability2': {'cooldown': 8, 'ready': True},
            'ultimate': {'cooldown': 30, 'ready': True}
        }