# Este manager se comunicaría con tu API de backend
class BrotherhoodManager:
    def __init__(self, api_client, player):
        self.api = api_client
        self.player = player
        self.brotherhood_data = None # Se llena con datos del servidor

    def fetch_brotherhood_data(self):
        # response = self.api.get(f"/brotherhoods/{self.player.brotherhood_id}")
        # self.brotherhood_data = response.json()
        # Ejemplo con datos falsos:
        self.brotherhood_data = {
            'name': 'Los Guardianes del Velo',
            'level': 5,
            'motd': '¡Por la Alianza!',
            'treasury': {'gold': 15000, 'resources': 2500},
            'members': [
                {'name': 'Player1', 'role': 'LIDER', 'level': 25},
                {'name': self.player.name, 'role': 'MIEMBRO', 'level': 20},
                {'name': 'Player3', 'role': 'RECLUTA', 'level': 18},
            ]
        }
        return self.brotherhood_data

    def donate_gold(self, amount):
        if self.player.gold >= amount:
            # self.api.post(f"/brotherhoods/donate", json={'gold': amount})
            self.player.gold -= amount
            self.brotherhood_data['treasury']['gold'] += amount
            print(f"Has donado {amount} de oro.")
            return True
        return False
