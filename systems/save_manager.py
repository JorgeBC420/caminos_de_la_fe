import pickle

def save_game(player, world):
    data = {
        'player': player.get_state(),
        'world': world.get_state()
    }
    with open('save.dat', 'wb') as f:
        pickle.dump(data, f)

def load_game():
    try:
        with open('save.dat', 'rb') as f:
            return pickle.load(f)
    except FileNotFoundError:
        print("No se encontró el archivo de guardado.")
        return None
