from ursina import *
from data.factions import FACTIONS
from entities.player import Player
from entities.enemy import Enemy
from entities.ui import GameUI

game_data = {
    'faction': None
}

def start_game():
    for entity in scene.entities:
        if isinstance(entity, (Button, Text)):
            destroy(entity)
    window.color = color.hex('#82C5FF')
    ground = Entity(model='plane', scale=(100, 1, 100), color=color.hex('#6A9A40'), texture='white_cube', texture_scale=(100,100), collider='box')
    player = Player(faction_name=game_data['faction'], position=(0, 0.5, 0))
    enemy1 = Enemy(position=(10, 0.5, 5), target=player)
    enemy2 = Enemy(position=(-5, 0.5, 10), target=player)
    ui = GameUI(player)

def faction_selection_screen():
    window.color = color.dark_gray
    Text("Caminos de la Fe: Cruzada y Conquista", scale=3, y=0.3)
    Text("Elige tu facción", scale=2, y=0.15)
    def select_faction(faction_name):
        game_data['faction'] = faction_name
        print(f"Facción seleccionada: {game_data['faction']}")
        start_game()
    Button('Cruzados', color=color.gold, scale=(0.3, 0.1), y=0, on_click=lambda: select_faction('Cruzados'))
    Button('Sarracenos', color=color.green, scale=(0.3, 0.1), y=-0.15, on_click=lambda: select_faction('Sarracenos'))
    Button('Antiguos', color=color.purple, scale=(0.3, 0.1), y=-0.3, on_click=lambda: select_faction('Antiguos'))