from ursina import *

class BrotherhoodUI(Entity):
    def __init__(self, manager, **kwargs):
        super().__init__(parent=camera.ui, **kwargs)
        self.manager = manager
        self.panel = Entity(parent=self, model='quad', scale=(1.2, 0.8), color=color.black90)
        Button(parent=self.panel, text='Miembros', position=(-0.4, 0.4), on_click=self.show_members)
        Button(parent=self.panel, text='Tesorería', position=(0, 0.4), on_click=self.show_treasury)
        Button(parent=self.panel, text='Cerrar', position=(0.4, 0.4), color=color.red, on_click=self.close)
        self.content_panel = Entity(parent=self.panel)
        self.show_members()

    def show_members(self):
        destroy(self.content_panel)
        self.content_panel = Entity(parent=self.panel)
        data = self.manager.fetch_brotherhood_data()
        Text(parent=self.content_panel, text=data['name'], y=0.3)
        for i, member in enumerate(data['members']):
            Text(parent=self.content_panel, text=f"{member['name']} ({member['role']}) - Nivel {member['level']}", y=0.2 - i*0.1, x=-0.5)

    def show_treasury(self):
        destroy(self.content_panel)
        self.content_panel = Entity(parent=self.panel)
        data = self.manager.brotherhood_data
        Text(parent=self.content_panel, text="Tesorería", y=0.3)
        Text(parent=self.content_panel, text=f"Oro: {data['treasury']['gold']}", y=0.2)
        self.donation_input = InputField(parent=self.content_panel, y=0)
        Button(parent=self.content_panel, text="Donar Oro", y=-0.1, on_click=self.donate)

    def donate(self):
        try:
            amount = int(self.donation_input.text)
            self.manager.donate_gold(amount)
            self.show_treasury()
        except ValueError:
            print("Por favor, introduce un número válido.")

    def close(self):
        destroy(self)
