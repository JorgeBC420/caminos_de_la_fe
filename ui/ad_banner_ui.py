from ursina import *

class AdBannerUI(Entity):
    def __init__(self, ad_manager, **kwargs):
        super().__init__(parent=camera.ui, **kwargs)
        self.ad_manager = ad_manager
        self.panel = Entity(parent=self, model='quad', scale=(1.2, 0.08), color=color.rgb(255,230,120))
        self.text = Text(parent=self.panel, text='Publicidad: ¡Consigue oro extra viendo anuncios!', y=0.02, color=color.black)
        self.update_banner()

    def update_banner(self):
        if self.ad_manager.banner_active:
            self.panel.enabled = True
        else:
            self.panel.enabled = False
