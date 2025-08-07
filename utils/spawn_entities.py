from ursina import Entity
from utils.faction_colors import FACTION_COLORS

def spawn_mount(position, faction='cruzados', model='horse', **kwargs):
    colors = FACTION_COLORS.get(faction, [None, None])
    return Entity(model=model, position=position, color=colors[0], **kwargs)

def spawn_pet(position, pet_type='gato', model='sphere', flying=False, **kwargs):
    color_map = {
        'gato': (1, 0.8, 0.6, 1),
        'perro': (0.7, 0.5, 0.3, 1),
        'halcon': (0.8, 0.8, 0.2, 1),
        'dragoncito': (0.5, 0.2, 0.8, 1),
    }
    color = color_map.get(pet_type, (1, 1, 1, 1))
    e = Entity(model=model, position=position, color=color, **kwargs)
    if flying:
        e.y += 2
    return e
