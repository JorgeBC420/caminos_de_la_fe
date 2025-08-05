# from ursina import *

def show_dialogue(npc_name, text):
    print(f"[{npc_name}]: {text}")

def talk_to_npc(player):
    if player.faction == "Sarracenos" and player.level > 5:
        show_dialogue("Rashida", "Tu padre estaría orgulloso...")
    elif player.faction == "Cruzados":
        show_dialogue("Fray Luis", "La fe te guía, joven cruzado.")
    else:
        show_dialogue("NPC", "Bienvenido, viajero.")
# Clase NPC
