import requests
import time
from datetime import datetime, timedelta

class FactionWarClient:
    def __init__(self, api_url, auth_token=None):
        self.api_url = api_url
        self.auth_token = auth_token
        self.headers = {'Authorization': f'Bearer {auth_token}'} if auth_token else {}
        self.last_request_time = 0
        self.request_cooldown = 5

    def safe_request(self, method, endpoint, **kwargs):
        current_time = time.time()
        if current_time - self.last_request_time < self.request_cooldown:
            return None
        try:
            response = requests.request(
                method,
                f"{self.api_url}/{endpoint}",
                headers=self.headers,
                **kwargs
            )
            self.last_request_time = current_time
            if response.status_code == 429:
                print("Espera antes de enviar otra petición")
                return None
            return response
        except Exception as e:
            print(f"Error de conexión: {e}")
            return None
