from ursina import Entity, Button, camera
from utils.api_client import api_client

class MainMenuUI(Entity):
    def __init__(self, player):
        super().__init__(parent=camera.ui)
        self.player = player
        self.tabs = {
            "Stats": StatsPanel(player),
            "Entrenamiento": TrainingPanel(player),
            "Equipo": EquipmentPanel(player),
            "Inventario": InventoryPanel(player),
            "Estadísticas": PvPStatsPanel(player),
            "Hermandad": BrotherhoodPanel(player),
            "Misiones": MissionsPanel(player),
            "Ciudadela": CitadelPanel(player),
            "PvP": PvPPanel(player),
            "Guerra": WarPanel(player),
            "Salón de la Fama": FamePanel(player),
            "Mail": MailPanel(player),
            "Chat": ChatPanel(player)
        }
        self.current_tab = "Stats"
        self.create_tab_buttons()

    def create_tab_buttons(self):
        for i, tab_name in enumerate(self.tabs):
            btn = Button(
                text=tab_name,
                parent=self,
                position=(0.7, 0.4 - i*0.07),
                scale=(0.18, 0.05),
                on_click=lambda t=tab_name: self.switch_tab(t)
            )

    def switch_tab(self, tab_name):
        self.tabs[self.current_tab].disable()
        self.tabs[tab_name].enable()
        self.current_tab = tab_name

class StatsPanel(Entity):
    def __init__(self, player):
        super().__init__(parent=camera.ui)
        self.player = player
        self.disable()

    def enable(self):
        super().enable()
        self.load_data()

    def load_data(self):
        stats = api_client.get(f"/player/{self.player.id}/stats")
        # Actualiza la UI con los datos recibidos

class BrotherhoodPanel(Entity):
    def __init__(self, player):
        super().__init__(parent=camera.ui)
        self.player = player
        self.disable()

    def enable(self):
        super().enable()
        self.load_data()

    def load_data(self):
        brotherhood = api_client.get(f"/brotherhood/{self.player.brotherhood_id}")
        members = api_client.get(f"/brotherhood/{self.player.brotherhood_id}/members")
        alliances = api_client.get(f"/brotherhood/{self.player.brotherhood_id}/alliances")
        # Actualiza la UI con los datos recibidos

class MissionsPanel(Entity):
    def __init__(self, player):
        super().__init__(parent=camera.ui)
        self.player = player
        self.disable()

    def enable(self):
        super().enable()
        self.load_data()

    def load_data(self):
        missions = api_client.get(f"/missions/{self.player.id}")
        # Actualiza la UI con las misiones recibidas

# Repite este patrón para los demás paneles
