from ursina import *
from data.config import GameConfig

class Enemy(Entity):
    def __init__(self, position, target, **kwargs):
        super().__init__(**kwargs)
        self.model = 'sphere'
        self.color = color.red
        self.collider = 'box'
        self.position = position
        self.speed = GameConfig.ENEMY_SPEED
        self.health = GameConfig.ENEMY_HEALTH
        self.max_health = GameConfig.ENEMY_HEALTH
        self.target = target

    def update(self):
        if not self.target:
            return
        dist = distance(self, self.target)
        if dist > 2:
            self.look_at(self.target, axis='y')
            self.position += self.forward * self.speed * time.dt

    def take_damage(self, amount):
        self.health -= amount
        self.blink(color.white, duration=0.2)
        if self.health <= 0:
            self.die()

    def die(self):
        print("Enemigo derrotado!")
        destroy(self)