from ursina import *

class CitadelUI(Entity):
    def __init__(self, player, ui_manager, **kwargs):
        super().__init__(parent=camera.ui, **kwargs)
        self.player = player
        self.ui_manager = ui_manager
        Button(parent=self, model='quad', scale=99, color=color.black66, z=1)
        self.panel = Entity(parent=self, model='quad', scale=(1.5, 0.9), texture='assets/ui/panel_bg.png', z=0)
        self.content_area = Entity(parent=self.panel)
        Button(parent=self.panel, text='Estructuras', position=(-0.4, 0.4), on_click=self.show_structures_tab)
        Button(parent=self.panel, text='Beneficios', position=(-0.2, 0.4), on_click=self.show_benefits_tab)
        Button(parent=self.panel, text='Cerrar', position=(0.6, 0.4), color=color.red, on_click=self.close)
        self.show_structures_tab()

    def _clear_content(self):
        destroy(self.content_area)
        self.content_area = Entity(parent=self.panel)

    def show_structures_tab(self):
        self._clear_content()
        # Mock de estructuras
        structures = [
            {'name': 'Murallas', 'level': 3},
            {'name': 'Torre de Arqueros', 'level': 2},
            {'name': 'Almacén', 'level': 4},
        ]
        Text(parent=self.content_area, text="Estructuras de la Ciudadela", y=0.3)
        y = 0.15
        for s in structures:
            Text(parent=self.content_area, text=f"{s['name']} (Nivel {s['level']})", y=y, scale=1.2)
            y -= 0.08

    def show_benefits_tab(self):
        self._clear_content()
        # Mock de beneficios
        benefits = [
            'Bonificación de oro diario',
            'Reducción de daño en defensa',
            'Acceso a mercado especial',
        ]
        Text(parent=self.content_area, text="Beneficios de la Ciudadela", y=0.3)
        y = 0.15
        for b in benefits:
            Text(parent=self.content_area, text=f"- {b}", y=y, scale=1.2)
            y -= 0.08

    def close(self):
        destroy(self)
