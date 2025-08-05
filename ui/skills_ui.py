from ursina import *

class SkillButton(Button):
    def __init__(self, skill_name, cooldown, **kwargs):
        super().__init__(text=skill_name, **kwargs)
        self.cooldown = cooldown
        self.last_used = 0
        self.is_ready = True
        self.default_color = color.azure
        self.cooldown_color = color.gray
        self.update_visual()

    def use_skill(self):
        if self.is_ready:
            self.last_used = time.time()
            self.is_ready = False
            self.update_visual()
            invoke(self.reset_cooldown, delay=self.cooldown)
            return True
        return False

    def reset_cooldown(self):
        self.is_ready = True
        self.update_visual()

    def update_visual(self):
        self.color = self.default_color if self.is_ready else self.cooldown_color

    def update(self):
        # Actualiza el color si el cooldown terminó
        if not self.is_ready and time.time() - self.last_used >= self.cooldown:
            self.reset_cooldown()
