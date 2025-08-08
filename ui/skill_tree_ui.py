from ursina import *

class SkillTreeUI(Entity):
    def __init__(self, player, **kwargs):
        super().__init__(parent=camera.ui, **kwargs)
        self.player = player
        self.panel = Entity(parent=self, model='quad', scale=(1,0.8), color=color.dark_gray)
        Text(parent=self.panel, text='Árbol de Habilidades', y=0.35, scale=2)
        self.skill_points_text = Text(parent=self.panel, text=f"Puntos: {self.player.skill_points}", y=0.25)
        y = 0.1
        for skill in self.player.skill_tree:
            btn = Button(parent=self.panel, text=skill['name'], y=y, on_click=lambda s=skill: self.unlock_skill(s))
            y -= 0.12
        Button(parent=self.panel, text='Cerrar', y=-0.35, color=color.red, on_click=self.close)

    def unlock_skill(self, skill):
        if self.player.skill_points > 0 and not skill.get('unlocked', False):
            skill['unlocked'] = True
            self.player.skill_points -= 1
            self.skill_points_text.text = f"Puntos: {self.player.skill_points}"
            print(f"Habilidad desbloqueada: {skill['name']}")

    def close(self):
        destroy(self)
