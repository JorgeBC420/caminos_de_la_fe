from ursina import *
from ui.main_nav_bar import MainNavBar # Barra de navegación reutilizable

class CitadelScene(Entity):
    def __init__(self, player, game_manager, **kwargs):
        super().__init__(**kwargs)
        self.player = player
        self.game_manager = game_manager
        
        # --- Fondo de la escena ---
        # Usamos la imagen del mockup como fondo principal
        Entity(parent=self, model='quad', texture='assets/ui/citadel_mockup_bg.png', scale=(1.9, 1), z=10)

        # --- Paneles de Servicios (Herrero, etc.) ---
        # Botones para abrir los mercados y NPCs principales
        from ui.stable_ui import StableUI
        from ui.pet_ui import PetUI
        from ui.mount_market_ui import MountMarketUI
        from ui.potion_market_ui import PotionMarketUI
        from ui.weapon_market_ui import WeaponMarketUI
        from ui.armor_market_ui import ArmorMarketUI
        from ui.jewelry_market_ui import JewelryMarketUI
        from ui.npc_stable_ui import NPCStableUI
        from ui.npc_blacksmith_ui import NPCBlacksmithUI
        from ui.npc_armorer_ui import NPCArmorerUI
        from ui.npc_doctor_ui import NPCDoctorUI
        from ui.npc_pet_seller_ui import NPCPetSellerUI

        y_offset = 0.35
        btns = [
            ("Caballeriza (Gestión)", lambda: StableUI(self.player)),
            ("Guardería de Mascotas", lambda: PetUI(self.player)),
            ("Mercado de Monturas", lambda: MountMarketUI(self.player)),
            ("Mercado de Pociones", lambda: PotionMarketUI(self.player)),
            ("Mercado de Armas/Escudos", lambda: WeaponMarketUI(self.player)),
            ("Mercado de Armaduras", lambda: ArmorMarketUI(self.player)),
            ("Mercado de Joyas/Items", lambda: JewelryMarketUI(self.player)),
            ("Caballeriza (NPC)", lambda: NPCStableUI(self.player)),
            ("Herrero (NPC)", lambda: NPCBlacksmithUI(self.player)),
            ("Armero (NPC)", lambda: NPCArmorerUI(self.player)),
            ("Doctor (NPC)", lambda: NPCDoctorUI(self.player)),
            ("Vendedor de Mascotas (NPC)", lambda: NPCPetSellerUI(self.player)),
        ]
        for label, cb in btns:
            Button(parent=self, text=label, y=y_offset, x=-0.7, scale=(0.22, 0.06), on_click=cb)
            y_offset -= 0.09
        
        # --- Barra de Navegación Principal Inferior ---
        # Esta barra te permite cambiar a la escena de Perfil, abrir paneles, etc.
        self.nav_bar = MainNavBar(ui_manager=self.game_manager.ui_manager)

    def on_destroy(self):
        # Limpieza al salir de la escena
        destroy(self.nav_bar)
