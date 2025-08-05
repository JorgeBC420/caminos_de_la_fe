from ursina import Entity, Button, Text, camera, color, Func, destroy

class ProfileUI(Entity):
    def __init__(self, player):
        super().__init__(parent=camera.ui)
        self.player = player
        # Panel izquierdo
        self.left_panel = Entity(parent=self, model='quad', color=color.rgba(0,0,0,150), scale=(0.2,0.6), position=(-0.7,0))
        self.create_navigation_buttons()
        # Panel derecho
        self.right_panel = Entity(parent=self, model='quad', color=color.rgba(0,0,0,150), scale=(0.4,0.8), position=(0.3,0))
        self.update_stats()
        # Barra inferior
        self.create_bottom_bar()

    def create_navigation_buttons(self):
        buttons = [
            ('PERFIL', self.show_profile),
            ('EQUIPO', self.show_equipment),
            ('INVENTARIO', self.show_inventory),
            ('HABILIDADES', self.show_skills),
            ('HERMANDAD', self.show_brotherhood)
        ]
        for i, (text, action) in enumerate(buttons):
            Button(parent=self.left_panel, text=text, scale=(0.8,0.1), position=(0,0.4-i*0.2), on_click=action)

    def update_stats(self):
        for child in self.right_panel.children:
            destroy(child)
        stats = [
            f"Nivel: {getattr(self.player, 'level', 1)}",
            f"PS: {getattr(self.player, 'health', 100)}/{getattr(self.player, 'max_health', 100)}",
            f"Fuerza: {getattr(self.player, 'strength', 10)}",
            f"Defensa: {getattr(self.player, 'defense', 10)}",
            f"Velocidad: {getattr(self.player, 'speed', 10)}"
        ]
        for i, stat in enumerate(stats):
            Text(parent=self.right_panel, text=stat, position=(-0.4,0.4-i*0.1), origin=(-0.5,0.5))
        Button(parent=self.right_panel, text='+', scale=(0.1,0.1), position=(0.3,0.4), on_click=self.level_up)
        self.create_equipment_slots()

    def create_equipment_slots(self):
        slots = {'head': (-0.3,0.2), 'chest': (-0.3,0.0), 'weapon': (0.0,0.2), 'boots': (0.0,0.0)}
        for slot, pos in slots.items():
            item = getattr(self.player, 'equipment', {}).get(slot)
            icon = getattr(item, 'icon', 'empty_slot') if item else 'empty_slot'
            Button(parent=self.right_panel, texture=icon, scale=(0.15,0.15), position=pos, on_click=Func(self.open_inventory, slot))

    def create_bottom_bar(self):
        bottom_bar = Entity(parent=self, model='quad', color=color.rgba(0,0,0,200), scale=(0.8,0.1), position=(0,-0.45))
        buttons = [
            ('Hogar', self.go_home),
            ('Hermandad', self.go_brotherhood),
            ('Misiones', self.go_quests),
            ('Mapa', self.go_map)
        ]
        for i, (text, action) in enumerate(buttons):
            Button(parent=bottom_bar, text=text, scale=(0.2,0.8), position=(-0.6+i*0.4,0), on_click=action)

    def level_up(self):
        print("Subir de nivel!")
    def open_inventory(self, slot):
        print(f"Abrir inventario para slot: {slot}")
    def go_home(self):
        print("Ir a pantalla de hogar")
    def show_profile(self):
        print("Mostrar perfil")
    def show_equipment(self):
        print("Mostrar equipo")
    def show_inventory(self):
        print("Mostrar inventario")
    def show_skills(self):
        print("Mostrar habilidades")
    def show_brotherhood(self):
        print("Mostrar hermandad")
    def go_brotherhood(self):
        print("Ir a hermandad")
    def go_quests(self):
        print("Ir a misiones")
    def go_map(self):
        print("Ir a mapa")
