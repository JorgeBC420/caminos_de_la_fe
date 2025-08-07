from ursina import *
from data.mount_data import MOUNT_DATA

class NPCStableUI(Entity):
    def __init__(self, player, **kwargs):
        super().__init__(parent=camera.ui, **kwargs)
        self.player = player
        self.panel = Entity(parent=self, model='quad', scale=(0.8, 0.7), color=color.brown.tint(-.2))
        Text(parent=self.panel, text='Caballeriza (NPC)', y=0.3, scale=1.5)
        # Ejemplo de montura a la venta
        from data.mount_data import MOUNT_DATA
        self.npc_mounts = [
            {'key': 'caballo_comun', 'price': 5000},
            {'key': 'corcel_de_guerra', 'price': 20000},
        ]
        y_offset = 0.1
        for offer in self.npc_mounts:
            data = MOUNT_DATA[offer['key']]
            btn_text = f"{data['name']} (Nivel {data['unlock_level']}) - {offer['price']} oro"
            Button(parent=self.panel, text=btn_text, y=y_offset, on_click=lambda o=offer: self.buy_mount(o))
            y_offset -= 0.12

    def buy_mount(self, offer):
        from data.mount_data import MOUNT_DATA
        data = MOUNT_DATA[offer['key']]
        player_level = self.player.level
        unlock_level = data['unlock_level']
        price = offer['price']
        if player_level < unlock_level:
            print(f"Necesitas ser nivel {unlock_level} para comprar esta montura.")
            return
        if self.player.gold >= price:
            self.player.gold -= price
            from inventory.inventory_manager import InventoryItem
            item = InventoryItem(item_id=offer['key'], name=data['name'], item_type='mount')
            self.player.inventory_manager.add_item(item)
            print(f"¡Montura {data['name']} comprada por {price} oro!")
        else:
            print("No tienes suficiente oro para comprar esta montura.")
        Button(parent=self.panel, text='Cerrar', y=-0.4, color=color.red, on_click=self.close)

    def close(self):
        destroy(self)
