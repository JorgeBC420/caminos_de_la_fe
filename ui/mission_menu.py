from ursina import *
from data.side_quests import SIDE_QUESTS

from data.mission_story import FACTION_INTROS

class MissionMenu(Entity):
    def __init__(self, on_select_main=None, on_select_side=None, player_faction='cruzado', **kwargs):
        super().__init__(parent=camera.ui, **kwargs)
        self.on_select_main = on_select_main
        self.on_select_side = on_select_side
        self.player_faction = player_faction
        self._create_ui()

    def _create_ui(self):
        Text('Menú de Misiones', y=0.45, origin=(0,0), scale=2)
        # Mostrar trasfondo de facción antes de avanzar
        intro = FACTION_INTROS.get(self.player_faction, FACTION_INTROS['cruzado'])
        self.intro_text = Text(
            text=f"{intro['mentalidad']}\n\n{intro['inicio']}\n\n{intro['mentor_dialogue']}",
            y=0.32,
            origin=(0,0),
            scale=1.1,
            color=color.white,
            background=True,
            background_color=color.black33,
            wordwrap=40
        )
        # Botón de misiones principales
        self.main_btn = Button(text='Misiones Principales', position=(-0.4, 0.08), scale=(0.5,0.12), color=color.gold)
        self.main_btn.on_click = self._select_main
        # Botón de misiones secundarias
        self.side_btn = Button(text='Misiones Secundarias', position=(0.4, 0.08), scale=(0.5,0.12), color=color.azure)
        self.side_btn.on_click = self._select_side

    def _select_main(self):
        if self.on_select_main:
            self.on_select_main()
        destroy(self)

    def _select_side(self):
        if self.on_select_side:
            self.on_select_side()
        destroy(self)

class SideQuestUI(Entity):
    def __init__(self, **kwargs):
        super().__init__(parent=camera.ui, **kwargs)
        self._create_ui()

    def _create_ui(self):
        Text('Misiones Secundarias', y=0.45, origin=(0,0), scale=2)
        for i, quest in enumerate(SIDE_QUESTS):
            btn = Button(text=quest['name'], position=(0, 0.3 - i*0.13), scale=(0.7,0.1), color=color.lime)
            btn.on_click = lambda q=quest: self._show_details(q)

    def _show_details(self, quest):
        window = WindowPanel(title=quest['name'], content=Text(quest['description'], scale=1.2), position=(0,0), scale=(0.7,0.3))
