class EventSystem:
    def __init__(self):
        self.active_events = []

    def add_event(self, event):
        self.active_events.append(event)

    def claim_event_reward(self, player, event):
        # Lógica para dar recompensa
        pass
