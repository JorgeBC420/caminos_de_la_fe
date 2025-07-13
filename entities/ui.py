from ursina import *

class HealthBar(Entity):
    def __init__(self, max_value, **kwargs):
        super().__init__(parent=camera.ui, model='quad', color=color.black, scale=(0.5, 0.04), **kwargs)
        self.bar = Entity(parent=self, model='quad', color=color.red, scale=(1, 1), z=-0.1)
        self._max_value = max_value
        self._value = max_value

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, new_value):
        self._value = max(0, new_value)
        self.bar.scale_x = self._value / self._max_value
        if self.bar.scale_x < 0.3:
            self.bar.color = color.orange
        elif self.bar.scale_x < 0.6:
            self.bar.color = color.yellow
        else:
            self.bar.color = color.green

class GameUI:
    def __init__(self, player):
        self.player = player
        self.setup_health_bar()

    def setup_health_bar(self):
        self.health_bar = HealthBar(
            max_value=self.player.max_health,
            position=window.bottom_left + Vec2(0.28, 0.07)
        )
        # Aquí podrías agregar más elementos de UI