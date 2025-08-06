from ursina import Entity
from datetime import datetime, timedelta

class LegendaryItem(Entity):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.current_owner = None
        self.stolen_time = None
        self.protected_until = None
        self.purification_time = None

    def on_stolen(self, new_owner):
        self.current_owner = new_owner
        self.stolen_time = datetime.now()
        self.protected_until = self.stolen_time + timedelta(hours=12)
        self.purification_time = None
        new_owner.add_debuff("Maldición del Saqueador", {
            'duration': 7200,
            'stats_penalty': 0.15
        })

    def start_purification(self):
        self.purification_time = datetime.now()

    def is_stealable(self):
        now = datetime.now()
        return (
            self.current_owner and
            self.protected_until and
            now > self.protected_until and
            (not self.purification_time or now > self.purification_time + timedelta(hours=2))
        )
