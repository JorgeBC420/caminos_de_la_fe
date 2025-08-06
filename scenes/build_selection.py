from ursina import *
from data.basic_abilities import BASIC_ABILITIES
from data.ultimate_abilities import ULTIMATE_ABILITIES

class BuildSelection(Entity):
    def __init__(self, faction_name, on_confirm, presets=None, **kwargs):
        super().__init__(parent=camera.ui, **kwargs)
        self.faction = faction_name
        self.on_confirm = on_confirm
        self.presets = presets
        self.selected_basics = []
        self.selected_ultimate = None
        if self.presets:
            self._create_presets_ui()
        else:
            self._create_free_ui()

    def _create_presets_ui(self):
        Text('Elige tu build favorito:', y=0.4, origin=(0,0), scale=2)
        for i, opt in enumerate(self.presets):
            btn = Button(
                text=opt['label'],
                position=(0, 0.2 - i*0.15),
                scale=(0.8, 0.13),
                color=color.azure
            )
            btn.on_click = lambda opt=opt: self._select_preset(opt)

    def _select_preset(self, opt):
        self.selected = opt['build']
        self._confirm_btn()

    def _confirm_btn(self):
        if self.selected:
            self.on_confirm(self.selected)
            destroy(self)

    def _create_free_ui(self):
        Text(f'Selecciona 2 habilidades básicas ({self.faction})', y=0.4, origin=(0,0), scale=2)
        basics = BASIC_ABILITIES[self.faction]
        for i, ab in enumerate(basics):
            btn = Button(text=ab['name'], position=(-0.66 + i*0.66, 0.2), scale=(0.6,0.1), color=color.azure)
            btn.ability_key = ab['key']
            btn.on_click = self._toggle_basic(btn)
        Text('Selecciona 1 Ultimate', y=0.0, origin=(0,0), scale=2)
        ult = ULTIMATE_ABILITIES[self.faction]
        self.ult_button = Button(text=ult['name'], position=(0, -0.1), scale=(0.8,0.1), color=color.orange)
        self.ult_button.ability_key = ult['key']
        self.ult_button.on_click = self._toggle_ultimate(self.ult_button)
        self.confirm_btn = Button(text='Confirmar Build', position=(0, -0.4), scale=(0.8,0.1), color=color.lime, enabled=False)
        self.confirm_btn.on_click = self._confirm

    def _toggle_basic(self, btn):
        def fn():
            key = btn.ability_key
            if key in self.selected_basics:
                self.selected_basics.remove(key)
                btn.color = color.azure
            else:
                if len(self.selected_basics) >= 2:
                    return
                self.selected_basics.append(key)
                btn.color = color.lime
            self._update_confirm()
        return fn

    def _toggle_ultimate(self, btn):
        def fn():
            key = btn.ability_key
            if self.selected_ultimate == key:
                self.selected_ultimate = None
                btn.color = color.orange
            else:
                self.selected_ultimate = key
                btn.color = color.violet
            self._update_confirm()
        return fn

    def _update_confirm(self):
        valid = (len(self.selected_basics) == 2 and self.selected_ultimate is not None)
        self.confirm_btn.enabled = valid

    def _confirm(self):
        build = {
            'basics': self.selected_basics.copy(),
            'ultimate': self.selected_ultimate
        }
        self.on_confirm(build)
        destroy(self)
