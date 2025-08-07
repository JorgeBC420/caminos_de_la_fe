from ursina import *

class BrotherhoodUI(Entity):
    def __init__(self, player, ui_manager, **kwargs):
        super().__init__(parent=camera.ui, **kwargs)
        self.player = player
        self.ui_manager = ui_manager

        # Fondo modal que bloquea la interacción con lo que hay detrás
        Button(parent=self, model='quad', scale=99, color=color.black66, z=1)

        # Panel principal
        self.panel = Entity(parent=self, model='quad', scale=(1.5, 0.9), texture='assets/ui/panel_bg.png', z=0)
        
        # --- Lógica de Pestañas ---
        self.content_area = Entity(parent=self.panel) # Contenedor para el contenido de la pestaña

        # Botones de las pestañas
        Button(parent=self.panel, text='Miembros', position=(-0.4, 0.4), on_click=self.show_members_tab)
        Button(parent=self.panel, text='Tesorería', position=(-0.2, 0.4), on_click=self.show_treasury_tab)
        Button(parent=self.panel, text='Cancillería', position=(0, 0.4), on_click=self.show_chancellery_tab)
        
        Button(parent=self.panel, text='Cerrar', position=(0.6, 0.4), color=color.red, on_click=self.close)

        self.show_members_tab() # Mostrar la primera pestaña por defecto

    def _clear_content(self):
        destroy(self.content_area)
        self.content_area = Entity(parent=self.panel)

    def show_members_tab(self):
        self._clear_content()
        Text(parent=self.content_area, text="Lista de Miembros", y=0.3)
        # ... Lógica para obtener y mostrar la lista de miembros del clan desde el backend

    def show_treasury_tab(self):
        self._clear_content()
        Text(parent=self.content_area, text="Tesorería de la Hermandad", y=0.3)
        # ... Lógica para mostrar oro, recursos y permitir donaciones

    def show_chancellery_tab(self):
        self._clear_content()
        Text(parent=self.content_area, text="Diplomacia y Guerra", y=0.3)
        # ... Lógica para declarar guerra o proponer alianzas

    def close(self):
        destroy(self)
