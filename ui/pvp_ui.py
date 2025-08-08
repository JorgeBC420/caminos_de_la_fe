from ursina import *

class PvPUI(Entity):
    def __init__(self, manager, **kwargs):
        super().__init__(parent=camera.ui, **kwargs)
        self.manager = manager
        self.panel = Entity(parent=self, model='quad', scale=(0.6, 0.4), color=color.red.tint(-0.5))
        Button(parent=self.panel, text="Buscar Duelo", scale=(0.4, 0.2), on_click=self.find_match)
        self.result_text = Text(parent=self.panel, y=-0.2)
    def find_match(self):
        # Simulación de resultado PvP
        import random
        victory = random.choice([True, False])
        result = {
            'victory': victory,
            'opponent_name': 'JugadorX',
            'elo_change': random.randint(-20, 30) if not victory else random.randint(10, 40)
        }
        if result['victory']:
            self.result_text.text = f"¡Victoria contra {result['opponent_name']}! \nELO: +{result['elo_change']}"
        else:
            self.result_text.text = f"Derrota contra {result['opponent_name']}. \nELO: {result['elo_change']}"
