from ursina import Entity
import time

class LegendaryItem(Entity):
    def __init__(self, item_type):
        super().__init__()
        self.item_type = item_type
        self.protection_end_time = 0
        self.owner = None
    
    def on_stolen(self, new_owner):
        if time.time() > self.protection_end_time:
            self.owner = new_owner
            self.start_purification()
    
    def start_purification(self):
        print(f"Purificación iniciada para {self.owner}")
