from ursina import *
from ursina import Button
import json

class MissionSelectionUI(Entity):
    def __init__(self):
        super().__init__()
        self.background = Entity(parent=self, model='quad', color=color.dark_gray, scale=(0.6,0.6), position=(0,0,0))
        self.title = Text(text='Misiones Disponibles', parent=self, position=(0,0.25), scale=2)
        self.mission_buttons = []
        self.load_missions()

    def load_missions(self):
        missions = []
        for fname in [
            'client/data/missions/mission_tutorial.json',
            'client/data/missions/mission_story.json',
            'client/data/missions/mission_side.json'
        ]:
            try:
                with open(fname, 'r', encoding='utf-8') as f:
                    missions.extend(json.load(f))
            except Exception:
                pass
        y = 0.1
        for mission in missions:
            btn = Button(text=mission['name'], parent=self, position=(0,y), scale=(0.4,0.1), on_click=lambda m=mission: self.accept_mission(m))
            self.mission_buttons.append(btn)
            y -= 0.15

    def accept_mission(self, mission_data):
        from client.core.game_manager import GameManager
        GameManager.instance().launch_mission(mission_data)
        self.disable()
