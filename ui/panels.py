from ursina import Entity, camera
from utils.api_client import api_client

class TrainingPanel(Entity):
    def __init__(self, player):
        super().__init__(parent=camera.ui)
        self.player = player
        self.disable()

    def enable(self):
        super().enable()
        self.load_data()

    def load_data(self):
        training_data = api_client.get(f"/training/{self.player.id}")
        # Actualiza la UI con los datos recibidos

class EquipmentPanel(Entity):
    def __init__(self, player):
        super().__init__(parent=camera.ui)
        self.player = player
        self.disable()

    def enable(self):
        super().enable()
        self.load_data()

    def load_data(self):
        equipment = api_client.get(f"/equipment/{self.player.id}")
        # Actualiza la UI con los datos recibidos

class InventoryPanel(Entity):
    def __init__(self, player):
        super().__init__(parent=camera.ui)
        self.player = player
        self.disable()

    def enable(self):
        super().enable()
        self.load_data()

    def load_data(self):
        inventory = api_client.get(f"/inventory/{self.player.id}")
        # Actualiza la UI con los datos recibidos

class PvPStatsPanel(Entity):
    def __init__(self, player):
        super().__init__(parent=camera.ui)
        self.player = player
        self.disable()

    def enable(self):
        super().enable()
        self.load_data()

    def load_data(self):
        pvp_stats = api_client.get(f"/pvp/{self.player.id}/stats")
        # Actualiza la UI con los datos recibidos

class CitadelPanel(Entity):
    def __init__(self, player):
        super().__init__(parent=camera.ui)
        self.player = player
        self.disable()

    def enable(self):
        super().enable()
        self.load_data()

    def load_data(self):
        citadel_data = api_client.get(f"/citadel/{self.player.id}")
        # Actualiza la UI con los datos recibidos

class PvPPanel(Entity):
    def __init__(self, player):
        super().__init__(parent=camera.ui)
        self.player = player
        self.disable()

    def enable(self):
        super().enable()
        self.load_data()

    def load_data(self):
        pvp_data = api_client.get(f"/pvp/{self.player.id}")
        # Actualiza la UI con los datos recibidos

class WarPanel(Entity):
    def __init__(self, player):
        super().__init__(parent=camera.ui)
        self.player = player
        self.disable()

    def enable(self):
        super().enable()
        self.load_data()

    def load_data(self):
        war_data = api_client.get(f"/war/{self.player.id}")
        # Actualiza la UI con los datos recibidos

class FamePanel(Entity):
    def __init__(self, player):
        super().__init__(parent=camera.ui)
        self.player = player
        self.disable()

    def enable(self):
        super().enable()
        self.load_data()

    def load_data(self):
        fame_data = api_client.get(f"/fame/{self.player.id}")
        # Actualiza la UI con los datos recibidos

class MailPanel(Entity):
    def __init__(self, player):
        super().__init__(parent=camera.ui)
        self.player = player
        self.disable()

    def enable(self):
        super().enable()
        self.load_data()

    def load_data(self):
        mail_data = api_client.get(f"/mail/{self.player.id}")
        # Actualiza la UI con los datos recibidos

class ChatPanel(Entity):
    def __init__(self, player):
        super().__init__(parent=camera.ui)
        self.player = player
        self.disable()

    def enable(self):
        super().enable()
        self.load_data()

    def load_data(self):
        chat_data = api_client.get(f"/chat/{self.player.id}")
        # Actualiza la UI con los datos recibidos
