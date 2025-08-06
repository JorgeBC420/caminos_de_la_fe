import time

class FaithPass:
    def __init__(self, player):
        self.player = player
        self.active = False
        self.expiry = None
        self.extra_slots = 0
        self.max_extra_slots = 3

    def activate(self):
        self.active = True
        self.expiry = time.time() + 30*24*3600  # 1 mes
        self.player.ads_disabled_until = time.time() + 6*30*24*3600  # 6 meses
        print('Faith Pass activado')

    def is_active(self):
        return self.active and time.time() < self.expiry

    def add_extra_slot(self):
        if self.extra_slots < self.max_extra_slots:
            self.extra_slots += 1
            print('Slot extra de misión añadido')

    def reset_daily(self):
        self.extra_slots = 0
