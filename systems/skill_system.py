from ursina import *

class SkillSystem:
    def __init__(self, player):
        self.player = player

    def golpe_purificador(self, target):
        # Daño extra y efecto visual
        damage = self.player.ataque * 2
        target.take_damage(damage)
        Entity(model='sphere', color=color.white, scale=0.5, position=target.position, duration=0.5)
        print("¡Golpe Purificador!")

    def egida_de_fe(self):
        # Buff temporal de defensa
        self.player.add_buff('egida_de_fe', {'defensa': 20}, duration=5)
        Entity(model='cube', color=color.azure, scale=1.2, position=self.player.position, duration=0.5)
        print("Égida de Fe: Defensa aumentada")

    def danza_de_cimitarras(self, target):
        # Ataque múltiple
        for i in range(3):
            target.take_damage(self.player.ataque)
            Entity(model='cube', color=color.orange, scale=0.2, position=target.position + Vec3(i*0.2,0,0), duration=0.2)
        print("¡Danza de Cimitarras!")

    def furia_del_jinn(self):
        # Invoca un pet temporal
        pet = Entity(model='sphere', color=color.magenta, scale=0.4, position=self.player.position + Vec3(1,0,0), duration=5)
        print("¡Furia del Jinn: Pet invocado!")

    def tormenta_de_arena(self, position):
        # Área de efecto
        aoe = Entity(model='circle', color=color.yellow, scale=2, position=position, duration=3)
        print("¡Tormenta de Arena: AoE creada!")
