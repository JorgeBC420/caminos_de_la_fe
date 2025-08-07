from ursina import *
from data.pet_data import PET_DATA

class PetUI(Entity):
    def __init__(self, player, **kwargs):
        super().__init__(parent=camera.ui, **kwargs)
        self.player = player
        self.panel = Entity(parent=self, model='quad', scale=(0.8, 0.7), color=color.lime.tint(-.2))
        Text(parent=self.panel, text='Guardería de Mascotas', y=0.3, scale=1.5)
        y_offset = 0.15
        for key, data in PET_DATA.items():
            unlock = self.player.level >= data['unlock_level']
            btn_text = f"{data['name']} (Nivel {data['unlock_level']})"
            if unlock:
                btn = Button(parent=self.panel, text=btn_text, y=y_offset, on_click=lambda k=key: self.select_pet(k))
            else:
                btn = Button(parent=self.panel, text=btn_text + ' (Bloqueado)', y=y_offset, color=color.gray, enabled=False)
            y_offset -= 0.12
        Button(parent=self.panel, text='Cerrar', y=-0.4, color=color.red, on_click=self.close)

    def select_pet(self, pet_key):
        # Aquí puedes agregar lógica para activar/cambiar mascota
        print(f"Seleccionar mascota: {pet_key}")
        # Ejemplo: self.player.set_active_pet(pet_key)

    def close(self):
        destroy(self)
