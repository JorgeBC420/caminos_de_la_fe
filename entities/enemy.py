from ursina import *
from data.config import GameConfig

class Enemy(Entity):
    def __init__(self, position, target, owner_scene=None, enemy_id=None, **kwargs):
        super().__init__(**kwargs)
        self.owner_scene = owner_scene
        self.enemy_id = enemy_id or 'enemy'
        try:
            self.model = load_model('Soldado SARRACENO.fbx')
        except Exception as e:
            print(f"Error al cargar modelo Soldado SARRACENO.fbx: {e}")
            self.model = 'sphere'
        self.color = color.red
        self.collider = 'box'
        self.position = position
        self.speed = GameConfig.ENEMY_SPEED
        self.health = GameConfig.ENEMY_HEALTH
        self.xp_value = GameConfig.XP_PER_ENEMY
        self.loot_table = ['herb', 'potion', 'gold']
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
        if self.owner_scene and hasattr(self.owner_scene, 'on_enemy_defeated'):
            self.owner_scene.on_enemy_defeated(self)
        if self.target and hasattr(self.target, 'add_experience'):
            self.target.add_experience(self.xp_value)
            # Lógica de loot simple
            import random
            if random.random() < GameConfig.LOOT_DROP_CHANCE:
                dropped_item = random.choice(self.loot_table)
                print(f"¡Loot obtenido: {dropped_item}!")
                if hasattr(self.target, 'inventory_manager'):
                    self.target.inventory_manager.add_item(dropped_item)
        if hasattr(self, 'health_bar'):
            destroy(self.health_bar)
        destroy(self)