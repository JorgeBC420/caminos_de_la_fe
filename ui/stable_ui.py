from ursina import *
from data.mount_data import MOUNT_DATA

class StableUI(Entity):
    def __init__(self, player, **kwargs):
        super().__init__(parent=camera.ui, **kwargs)
        self.player = player
        self.panel = Entity(parent=self, model='quad', scale=(0.8, 0.7), color=color.brown)
        Text(parent=self.panel, text='Caballeriza', y=0.3, scale=1.5)
        self.gold_text = Text(parent=self.panel, text=f'Oro: {self.player.gold}', y=0.2)
        y_offset = 0.1
        for key, data in MOUNT_DATA.items():
            unlock = self.player.level >= data['unlock_level']
            btn_text = f"{data['name']} (Nivel {data['unlock_level']})"
            if unlock:
                btn = Button(parent=self.panel, text=btn_text, y=y_offset, on_click=lambda k=key: self.buy_mount(k))
            else:
                btn = Button(parent=self.panel, text=btn_text + ' (Bloqueado)', y=y_offset, color=color.gray, enabled=False)
            y_offset -= 0.12
        Button(parent=self.panel, text='Cerrar', y=-0.4, color=color.red, on_click=self.close)

    def buy_mount(self, mount_key):
        data = MOUNT_DATA[mount_key]
        player_level = self.player.level
        unlock_level = data['unlock_level']
        cost = data['upgrade_costs'][0]
        if player_level < unlock_level:
            print(f"Necesitas ser nivel {unlock_level} para comprar esta montura.")
            return
        if self.player.gold >= cost:
            self.player.gold -= cost
            from inventory.inventory_manager import InventoryItem
            item = InventoryItem(item_id=mount_key, name=data['name'], item_type='mount')
            self.player.inventory_manager.add_item(item)
            print(f"¡Montura {data['name']} comprada!")
            self.gold_text.text = f'Oro: {self.player.gold}'
        else:
            print("No tienes suficiente oro.")

    def close(self):
        destroy(self)
