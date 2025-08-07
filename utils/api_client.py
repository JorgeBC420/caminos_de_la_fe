import requests

BASE_URL = "http://localhost:8000"  # Ajusta según tu backend

class APIClient:
    def get(self, endpoint):
        response = requests.get(BASE_URL + endpoint)
        return response.json()

    def post(self, endpoint, data=None):
        response = requests.post(BASE_URL + endpoint, json=data)
        return response.json()

api_client = APIClient()
