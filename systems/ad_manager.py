import time

class AdManager:
    def __init__(self):
        self.last_popup = time.time()
        self.popup_interval = 900  # 15 minutos
        self.banner_active = True
        self.daily_bonus_ads = 0
        self.max_daily_bonus = 3

    def should_show_popup(self):
        return time.time() - self.last_popup > self.popup_interval

    def show_popup(self):
        self.last_popup = time.time()
        # Aquí iría la lógica para mostrar el anuncio
        print('Mostrando anuncio pop-up')

    def show_banner(self):
        if self.banner_active:
            print('Banner activo en UI')

    def can_watch_bonus_ad(self):
        return self.daily_bonus_ads < self.max_daily_bonus

    def watch_bonus_ad(self, player):
        if self.can_watch_bonus_ad():
            self.daily_bonus_ads += 1
            player.gold += 100  # Bonificación por ver anuncio
            print('Oro extra por anuncio')
