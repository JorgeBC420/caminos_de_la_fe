from ursina import *

def render_auto_battle_cinematic(result, player, callback=None):
    scene = Entity(parent=camera.ui)
    background = Entity(parent=scene, model='quad', texture='battle_background', scale=(2, 1), z=1)
    combat_elements = []
    if result['victory']:
        animate_victory(scene, player, combat_elements)
    else:
        animate_defeat(scene, player, combat_elements)
    if callback:
        Button(parent=scene, text='Continuar', position=(0, -0.4), scale=(0.2, 0.1), on_click=callback)
    return scene

def animate_victory(scene, player, elements):
    pass

def animate_defeat(scene, player, elements):
    pass
