from ursina import *

class ShopUI(Entity):
    def __init__(self, player, faith_pass, ad_manager, **kwargs):
        super().__init__(parent=camera.ui, **kwargs)
        self.player = player
        self.faith_pass = faith_pass
        self.ad_manager = ad_manager
        self.panel = Entity(parent=self, model='quad', scale=(0.8, 0.7), color=color.gray)
        Text(parent=self.panel, text='Tienda', y=0.3, scale=1.5)
        self.gold_text = Text(parent=self.panel, text=f'Oro: {self.player.gold}', y=0.2)
        Button(parent=self.panel, text='Comprar 1000 oro ($1)', y=0.1, on_click=self.buy_gold)
        Button(parent=self.panel, text='Comprar Faith Pass ($10)', y=0.0, on_click=self.buy_faith_pass)
        Button(parent=self.panel, text='Ver anuncio para oro extra', y=-0.1, on_click=self.watch_ad)
        self.pass_text = Text(parent=self.panel, text=self.get_pass_status(), y=-0.2)
        Button(parent=self.panel, text='Cerrar', y=-0.3, color=color.red, on_click=self.close)

    def buy_gold(self):
        self.player.gold += 1000
        self.gold_text.text = f'Oro: {self.player.gold}'

    def buy_faith_pass(self):
        self.faith_pass.activate()
        self.pass_text.text = self.get_pass_status()

    def watch_ad(self):
        if self.ad_manager.can_watch_bonus_ad():
            self.ad_manager.watch_bonus_ad(self.player)
            self.gold_text.text = f'Oro: {self.player.gold}'
        else:
            print('Límite diario de anuncios alcanzado.')

    def get_pass_status(self):
        if self.faith_pass.is_active():
            return 'Faith Pass activo'
        return 'Faith Pass no adquirido'

    def close(self):
        destroy(self)
