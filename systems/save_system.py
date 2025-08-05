import pickle

def save_game(player):
    with open('save.dat', 'wb') as f:
        pickle.dump(player.stats, f)

def load_game(player):
    try:
        with open('save.dat', 'rb') as f:
            player.stats = pickle.load(f)
        print("Juego cargado correctamente.")
    except FileNotFoundError:
        print("No se encontró el archivo de guardado.")
