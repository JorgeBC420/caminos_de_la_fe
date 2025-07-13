from ursina import *
# CAMBIO: Importamos las escenas que vamos a gestionar
from scenes.faction_selection import FactionSelectionScreen
from scenes.combat_scene import CombatScene

class Game:
    def __init__(self):
        self.app = Ursina(
            title="Caminos de la Fe: Cruzada y Conquista",
            borderless=False,
            fullscreen=False,
        )
        self.game_data = {'faction': None}
        # CAMBIO: Añadimos un atributo para saber qué escena está activa
        self.current_scene = None

    def run(self):
        # Iniciar con la pantalla de selección de facción
        self.start_faction_selection()
        self.app.run()

    def start_faction_selection(self):
        """Inicia la pantalla de selección de facción."""
        print("Iniciando selección de facción...")
        
        # Si ya había una escena antes (ej: volver al menú), la limpiamos
        if self.current_scene and hasattr(self.current_scene, 'cleanup'):
            self.current_scene.cleanup()
        
        window.color = color.dark_gray
        # Creamos una instancia de FactionSelectionScreen y la guardamos
        self.current_scene = FactionSelectionScreen(game=self)

    # CAMBIO: Añadimos el método para iniciar la escena de combate
    def start_combat_scene(self):
        """Limpia la escena actual e inicia la escena de combate."""
        print("Iniciando escena de combate...")
        
        # La escena de selección de facción limpia sus propios botones al hacer clic.
        # Nos aseguramos de limpiar cualquier remanente por si acaso.
        for entity in scene.entities:
            if isinstance(entity, (Button, Text)):
                destroy(entity)

        window.color = color.hex('#82C5FF')
        # Creamos una instancia de CombatScene y la guardamos
        self.current_scene = CombatScene(game=self)


if __name__ == '__main__':
    juego = Game()
    juego.run()