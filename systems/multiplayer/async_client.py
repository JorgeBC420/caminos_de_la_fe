import requests

class AsyncClient:
    def __init__(self, api_url):
        self.base_url = api_url
    
    def join_war(self, player_data):
        response = requests.post(f"{self.base_url}/join_war", json=player_data)
        return response.json()

    def duel(self, player_data, opponent_id):
        response = requests.post(f"{self.base_url}/duel/{opponent_id}", json=player_data)
        return response.json()
