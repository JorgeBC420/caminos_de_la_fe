# /ui/virtual_joystick.py

from ursina import *
from math import sqrt

def distance(a, b):
    return sqrt((a[0] - b[0])**2 + (a[1] - b[1])**2)

class VirtualJoystick(Entity):
    def __init__(self, **kwargs):
        super().__init__(parent=camera.ui, **kwargs)

        # --- Elementos visuales del Joystick ---
        # La base estática del joystick
        self.background = Entity(
            parent=self,
            model='quad',
            texture='circle',
            color=color.white33,
            scale=0.25,
            position=(window.bottom_left.x + 0.2, window.bottom_left.y + 0.2, 0)
        )
        # El control móvil que el jugador arrastra
        self.knob = Entity(
            parent=self.background,
            model='quad',
            texture='circle',
            color=color.light_gray,
            scale=0.6
        )

        # --- Atributos de control ---
        self.is_active = False  # Para saber si el joystick está siendo usado
        self.max_distance = self.background.scale_x / 2 # El radio máximo que puede moverse el knob

        # El valor de salida del joystick (vector de dirección)
        self.value = Vec2(0, 0)

    def input(self, key):
        if key == 'left mouse down':
            # Si el clic está sobre el joystick, activarlo
            if distance(mouse.position, self.background.position) < self.max_distance:
                self.is_active = True
                self.knob.color = color.white

        if key == 'left mouse up':
            self.is_active = False
            self.knob.color = color.light_gray

    def update(self):
        if self.is_active:
            if distance(self.knob.position, Vec2(0,0)) > self.max_distance:
                self.knob.position = self.knob.position.normalized() * self.max_distance

            # Limitar el movimiento del knob al radio del fondo
            if distance(self.knob.position, Vec2(0,0)) > self.max_distance:
                self.knob.position = self.knob.position.normalized() * self.max_distance

            # Calcular el valor de salida normalizado (de -1 a 1)
            self.value = Vec2(
                self.knob.x / self.max_distance,
                self.knob.y / self.max_distance
            ).normalized()
        else:
            # Si no está activo, regresar el knob al centro y resetear el valor
            self.knob.position = lerp(self.knob.position, Vec2(0,0), time.dt * 10)
            self.value = Vec2(0,0)