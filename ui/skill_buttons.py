# /ui/skill_buttons.py

from ursina import *

def create_skill_buttons():
    """Crea y devuelve un diccionario con los botones de habilidad."""

    # Usamos window.bottom_right para posicionarlos en la esquina derecha
    base_pos = window.bottom_right - Vec2(0.2, -0.1)

    skill1 = Button(
        text='H1',
        scale=0.1,
        position=base_pos + Vec2(-0.24, 0),
        color=color.azure
    )
    skill1.on_click = lambda: print("Habilidad 1 activada!")

    skill2 = Button(
        text='H2',
        scale=0.1,
        position=base_pos + Vec2(-0.12, 0),
        color=color.azure
    )
    skill2.on_click = lambda: print("Habilidad 2 activada!")

    ultimate = Button(
        text='ULT',
        scale=0.12,
        position=base_pos,
        color=color.violet
    )
    ultimate.on_click = lambda: print("Ultimate activado!")

    return {'skill1': skill1, 'skill2': skill2, 'ultimate': ultimate}