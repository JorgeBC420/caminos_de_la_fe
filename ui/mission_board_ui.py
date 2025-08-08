from ursina import *

class MissionBoardUI(Entity):
    def __init__(self, game_manager, **kwargs):
        super().__init__(parent=camera.ui, **kwargs)
        self.game_manager = game_manager
        self.panel = Entity(parent=self, model='quad', scale=(0.7, 0.7), color=color.azure.tint(-.2))
        Text(parent=self.panel, text='Tablón de Misiones', y=0.3, scale=1.5)
        y_offset = 0.15
        # Cargar misión de ejemplo
        from core.mission_manager import MissionManager
        mm = game_manager.mission_manager if hasattr(game_manager, 'mission_manager') else MissionManager('default')
        mission = mm.load_mission('cq01_aethelgard')
        btn = Button(parent=self.panel, text=mission['name'], y=y_offset, on_click=lambda: self.accept_mission(mission['id']))
        Button(parent=self.panel, text='Cerrar', y=-0.4, color=color.red, on_click=self.close)

    def accept_mission(self, mission_id):
        print(f"Misión aceptada: {mission_id}")
        # Cargar datos de la misión y notificar al GameManager
        from core.mission_manager import MissionManager
        mm = self.game_manager.mission_manager if hasattr(self.game_manager, 'mission_manager') else MissionManager('default')
        mission_data = mm.load_mission(mission_id)
        if hasattr(self.game_manager, 'load_combat_scene'):
            self.game_manager.load_combat_scene(mission_data)
        else:
            print("GameManager no tiene método load_combat_scene")
        self.close()

    def close(self):
        destroy(self)
