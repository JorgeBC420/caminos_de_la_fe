import time

class EventSystem:
    events = {
        'holy_war': {'active': False, 'participants': []},
        'item_purification': {'player': None, 'timer': 0}
    }
    
    def start_event(self, event_name, data):
        self.events[event_name] = {**data, 'start_time': time.time()}
