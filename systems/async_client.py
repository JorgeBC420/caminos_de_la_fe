import requests
import threading
from threading import Thread
from queue import Queue
from systems.lang_manager import _

class AsyncGameClient:
    def __init__(self, server_url="http://localhost:8000"):
        self.server_url = server_url
        self.responses = Queue()
        self.player_id = None
    
    def register_player(self, player_data, callback):
        Thread(target=self._send_request, args=("POST", "/register", player_data, callback)).start()
    
    def join_holy_war(self, war_id, player_data, callback):
        Thread(target=self._send_request, args=("POST", f"/wars/{war_id}/join", player_data, callback)).start()
    
    def submit_duel(self, duel_data, callback):
        Thread(target=self._send_request, args=("POST", "/duels", duel_data, callback)).start()
    
    def get_battle_report(self, report_id, callback):
        Thread(target=self._send_request, args=("GET", f"/reports/{report_id}", {}, callback)).start()
    
    def _send_request(self, method, endpoint, data, callback):
        try:
            url = f"{self.server_url}{endpoint}"
            if method == "POST":
                response = requests.post(url, json=data)
            else:
                response = requests.get(url)
            if response.status_code == 200:
                callback(response.json())
            else:
                print(_("network_error"))
        except Exception as e:
            print(f"Network error: {e}")
