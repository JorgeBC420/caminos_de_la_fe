from ursina import *

class PlayerStatusUI(Entity):
    def __init__(self, player, faith_pass, progression_limits, **kwargs):
        super().__init__(parent=camera.ui, **kwargs)
        self.player = player
        self.faith_pass = faith_pass
        self.progression_limits = progression_limits
        self.panel = Entity(parent=self, model='quad', scale=(0.7, 0.2), color=color.black33)
        self.gold_text = Text(parent=self.panel, text=f'Oro: {self.player.gold}', x=-0.3, y=0.08)
        self.pass_text = Text(parent=self.panel, text=self.get_pass_status(), x=0.0, y=0.08)
        self.mission_text = Text(parent=self.panel, text=self.get_mission_status(), x=0.3, y=0.08)
        self.update_status()

    def update_status(self):
        self.gold_text.text = f'Oro: {self.player.gold}'
        self.pass_text.text = self.get_pass_status()
        self.mission_text.text = self.get_mission_status()

    def get_pass_status(self):
        if self.faith_pass.is_active():
            return 'Faith Pass: Activo'
        return 'Faith Pass: No'

    def get_mission_status(self):
        limit = self.progression_limits.daily_mission_limit
        if self.faith_pass.is_active():
            limit += 3 + self.faith_pass.extra_slots
        return f'Misiones hoy: {self.progression_limits.missions_completed_today}/{limit}'
