import requests

class APIClient:
    def __init__(self, base_url, auth_token=None):
        self.base_url = base_url
        self.headers = {'Authorization': f'Bearer {auth_token}'} if auth_token else {}

    def get_current_war(self):
        url = f"{self.base_url}/current_war"
        response = requests.get(url, headers=self.headers)
        return response.json() if response.ok else None

    def submit_power(self, faction, power):
        url = f"{self.base_url}/submit_power"
        response = requests.post(url, json={'faction': faction, 'power': power}, headers=self.headers)
        return response.json() if response.ok else None

    def claim_daily_reward(self):
        url = f"{self.base_url}/claim_daily_reward"
        response = requests.post(url, headers=self.headers)
        return response.json() if response.ok else None
