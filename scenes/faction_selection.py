# Pantalla de selección de facción
# /scenes/faction_selection.py


from ursina import *
from data.mission_story import FACTION_INTROS
from data.basic_abilities import BASIC_ABILITIES
from data.ultimate_abilities import ULTIMATE_ABILITIES

class FactionSelectionScreen(Entity):
    def __init__(self, game, **kwargs):
        super().__init__(parent=scene, **kwargs)
        self.game = game
        self.selected_faction = 'cruzado'

        Text("Caminos de la Fe: Cruzada y Conquista", scale=3, y=0.3)
        Text("Elige tu facción", scale=2, y=0.15)

        self.cruzado_btn = Button('Cruzados', color=color.gold, scale=(0.3, 0.1), y=0, on_click=lambda: self.show_faction('cruzado'))
        self.sarraceno_btn = Button('Sarracenos', color=color.green, scale=(0.3, 0.1), y=-0.15, on_click=lambda: self.show_faction('sarraceno'))
        self.antiguo_btn = Button('Antiguos', color=color.magenta, scale=(0.3, 0.1), y=-0.3, on_click=lambda: self.show_faction('antiguo'))

        self.desc_text = Text('', y=-0.55, origin=(0,0), scale=1.1, color=color.white, background=True, background_color=color.black33, wordwrap=40)
        self.abilities_text = Text('', y=-0.8, origin=(0,0), scale=1, color=color.azure, wordwrap=40)
        self.ultimate_text = Text('', y=-1.05, origin=(0,0), scale=1, color=color.gold, wordwrap=40)
        self.preview_text = Text('', y=0.55, origin=(0,0), scale=1.2, color=color.yellow, wordwrap=40)
        self.show_faction('cruzado')

        self.start_btn = Button('Comenzar', color=color.orange, scale=(0.25, 0.09), y=-1.25, on_click=self.start_game)

    def show_faction(self, faction_key):
        self.selected_faction = faction_key
        intro = FACTION_INTROS.get(faction_key, FACTION_INTROS['cruzado'])
        self.preview_text.text = f"Vas a seleccionar: {faction_key.capitalize()}"
        self.desc_text.text = f"{intro['mentalidad']}\n\n{intro['inicio']}\n\n{intro['mentor_dialogue']}"
        abilities = BASIC_ABILITIES.get(faction_key.capitalize(), {})
        if abilities:
            abilities_str = '\n'.join([f"- {name}: {desc['description']}" for name, desc in abilities.items()])
            self.abilities_text.text = f"Habilidades básicas:\n{abilities_str}"
        else:
            self.abilities_text.text = "Habilidades básicas: No disponibles."
        ultimates = ULTIMATE_ABILITIES.get(faction_key.capitalize(), {})
        if ultimates:
            ultimate_str = '\n'.join([f"- {name}: {desc['description']}" for name, desc in ultimates.items()])
            self.ultimate_text.text = f"Habilidad Ultimate:\n{ultimate_str}"
        else:
            self.ultimate_text.text = "Habilidad Ultimate: No disponible."

    def start_game(self):
        # Si game_data es dict, conviértelo a GameData
        try:
            from data.game_data import GameData
            if not isinstance(self.game.game_data, GameData):
                gd = GameData()
                gd.set_faction(self.selected_faction.capitalize())
                # Inicializar habilidades básicas
                abilities = BASIC_ABILITIES.get(self.selected_faction.capitalize(), {})
                for name in abilities:
                    gd.unlock_ability(name)
                # Inicializar ultimate
                ultimates = ULTIMATE_ABILITIES.get(self.selected_faction.capitalize(), {})
                if ultimates:
                    first_ultimate = next(iter(ultimates.keys()))
                    gd.set_ultimate(first_ultimate)
                self.game.game_data = gd
        except Exception as e:
            print(f"Error inicializando GameData: {e}")
        print(f"Facción seleccionada: {getattr(self.game.game_data, 'faction', self.selected_faction.capitalize())}")
        print(f"Habilidades iniciales: {getattr(self.game.game_data, 'abilities', [])}")
        print(f"Ultimate inicial: {getattr(self.game.game_data, 'ultimate', None)}")
        self.game.start_combat_scene()

    # ...el método select_faction se reemplaza por show_faction y start_game...