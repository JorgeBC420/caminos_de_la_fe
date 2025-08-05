import pickle

class GuestPlayer:
    def __init__(self):
        self.name = 'Invitado'
        self.stats = {'nivel': 1, 'fuerza': 10, 'defensa': 8}
        self.inventory = []
        self.progress = {}

    def get_state(self):
        return {
            'name': self.name,
            'stats': self.stats,
            'inventory': self.inventory,
            'progress': self.progress
        }

    def save_local(self):
        with open('guest_save.dat', 'wb') as f:
            pickle.dump(self.get_state(), f)
        print('Progreso de invitado guardado localmente.')

    def load_local(self):
        try:
            with open('guest_save.dat', 'rb') as f:
                state = pickle.load(f)
            self.name = state['name']
            self.stats = state['stats']
            self.inventory = state['inventory']
            self.progress = state['progress']
            print('Progreso de invitado cargado.')
        except FileNotFoundError:
            print('No hay partida de invitado guardada.')
