# Efectos visuales para armas e ítems legendarios
# Usar en combinación con Ursina y ParticleSystem

from ursina import *

def show_chalice_effect(entity):
    # Aura dorada y partículas de cruces
    aura = Entity(parent=entity, model='sphere', color=color.gold, scale=1.2, alpha=0.3)
    ParticleSystem(position=entity.position, texture='particle_flare', count=20, color=color.gold, speed=0.3, lifespan=1.2)
    Audio('holy_blast.wav', volume=0.7)
    invoke(aura.disable, delay=2)

def show_mirror_effect(entity):
    # Espejismo y distorsión de aire
    ParticleSystem(position=entity.position, texture='sand_particle', count=15, color=color.azure, speed=0.2, lifespan=1.0)
    Audio('desert_wind.wav', volume=0.5)

def show_mask_effect(entity):
    # Aura de sombras y ojos brillantes
    aura = Entity(parent=entity, model='sphere', color=color.black, scale=1.1, alpha=0.4)
    ParticleSystem(position=entity.position, texture='smoke', count=18, color=color.black, speed=0.2, lifespan=1.5)
    Audio('dark_whisper.wav', volume=0.6)
    invoke(aura.disable, delay=2)
