from datetime import datetime, timedelta

class LegendaryItem:
    def __init__(self, item_id, name, owner=None):
        self.item_id = item_id
        self.name = name
        self.current_owner = owner
        self.stolen_time = None
        self.protected_until = None
        self.purification_time = None
        self.history = []  # Para ranking de cazadores

    def on_stolen(self, new_owner):
        self.current_owner = new_owner
        self.stolen_time = datetime.now()
        self.protected_until = self.stolen_time + timedelta(hours=12)
        self.purification_time = None
        self.history.append({'event': 'stolen', 'owner': new_owner, 'time': self.stolen_time})
        # Notificación global (simulada)
        print(f"¡{self.name} ha sido robado por {new_owner.name}!")
        new_owner.add_debuff("Maldición del Saqueador", {'duration': 7200, 'stats_penalty': 0.15})

    def start_purification(self):
        self.purification_time = datetime.now()
        self.history.append({'event': 'purification', 'owner': self.current_owner, 'time': self.purification_time})

    def is_stealable(self):
        now = datetime.now()
        return (
            self.current_owner and
            self.protected_until and
            now > self.protected_until and
            (not self.purification_time or now > self.purification_time + timedelta(hours=2))
        )

    def get_ranking(self):
        # Devuelve ranking de cazadores por cantidad de recuperaciones
        from collections import Counter
        owners = [h['owner'].name for h in self.history if h['event'] == 'stolen']
        return Counter(owners)
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
