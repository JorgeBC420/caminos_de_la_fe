from ursina import Entity, Text, Button, color, camera

class LevelUpUI(Entity):
    def __init__(self, player, on_confirm=None):
        super().__init__(parent=camera.ui)
        self.player = player
        self.temp_stats = player.stats.copy()
        self.skill_points = getattr(player, 'skill_points', 5)
        self.on_confirm = on_confirm
        self.bg = Entity(model='quad', color=color.rgba(0,0,0,180), scale=(0.7,0.7), position=(0,0,2))
        self.stat_texts = []
        self.plus_buttons = []
        y_start = 0.2
        for i, stat in enumerate(self.temp_stats):
            t = Text(text=f"{stat}: {self.temp_stats[stat]}", parent=self.bg, position=(-0.2, y_start-i*0.15), scale=1.2)
            self.stat_texts.append(t)
            def add_point(s=stat, idx=i):
                if self.skill_points > 0:
                    self.temp_stats[s] += 1
                    self.skill_points -= 1
                    self.stat_texts[idx].text = f"{s}: {self.temp_stats[s]}"
            btn = Button(text='+', parent=self.bg, position=(0.2, y_start-i*0.15), scale=(0.1,0.1), on_click=add_point)
            self.plus_buttons.append(btn)
        self.confirm_btn = Button(text='Confirmar', parent=self.bg, position=(0,-0.3), scale=(0.3,0.1), color=color.green, on_click=self.confirm)
    def confirm(self):
        for stat in self.temp_stats:
            self.player.stats[stat] = self.temp_stats[stat]
        if self.on_confirm:
            self.on_confirm()
        self.disable()
        self.bg.disable()
        for t in self.stat_texts: t.disable()
        for b in self.plus_buttons: b.disable()
        self.confirm_btn.disable()
