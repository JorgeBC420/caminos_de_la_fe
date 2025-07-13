from ursina import *
from core.game_controller import faction_selection_screen

def main():
    app = Ursina()
    Text("Caminos de la Fe: ¡Bienvenido!", origin=(0, 0), scale=2)
    app.run()

if __name__ == '__main__':
    main()
