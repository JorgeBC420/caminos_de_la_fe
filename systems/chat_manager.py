class ChatManager:
    def __init__(self, api_client, player):
        self.api = api_client
        self.player = player
        self.messages = []
    def send_message(self, channel, message):
        # self.api.post(f"/chat/{channel}", json={'player': self.player.name, 'message': message})
        self.messages.append({'channel': channel, 'player': self.player.name, 'message': message})
    def fetch_messages(self, channel):
        # response = self.api.get(f"/chat/{channel}")
        # return response.json()
        return [m for m in self.messages if m['channel'] == channel]
