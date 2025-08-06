from ursina import *

class CombatScene(Entity):
    def __init__(self, mission_data):
        super().__init__()
        self.mission_data = mission_data
        self.enemies = []
        self.completed = False
        self.setup_combat()

    def setup_combat(self):
        y = 0.3
        for enemy_name in self.mission_data.get('enemies', []):
            enemy = Button(text=enemy_name, position=(0,y), scale=(0.2,0.1), on_click=lambda e=enemy_name: self.defeat_enemy(e))
            self.enemies.append(enemy)
            y -= 0.15
        self.status = Text(text='Derrota a todos los enemigos', position=(0,0.45), scale=1.5)

    def defeat_enemy(self, enemy_name):
        for btn in self.enemies:
            if btn.text == enemy_name:
                btn.disable()
        if all(not btn.enabled for btn in self.enemies):
            self.complete_mission()

    def complete_mission(self):
        self.completed = True
        self.status.text = '¡Misión completada!'
        from client.core.game_manager import GameManager
        GameManager.instance().mission_complete({
            'xp': self.mission_data.get('xp_reward', 0),
            'loot': self.mission_data.get('loot', [])
        })
        invoke(self.disable, delay=2)
