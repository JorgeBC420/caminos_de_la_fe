from ursina import *
from data.mount_data import MOUNT_DATA

class MountMarketUI(Entity):
    def __init__(self, player, **kwargs):
        super().__init__(parent=camera.ui, **kwargs)
        self.player = player
        self.panel = Entity(parent=self, model='quad', scale=(0.8, 0.7), color=color.azure.tint(-.2))
        Text(parent=self.panel, text='Mercado de Monturas (P2P)', y=0.3, scale=1.5)
        # Simulación de monturas en venta (debería venir de la base de datos o red)
        from data.mount_data import MOUNT_DATA
        self.market_mounts = [
            {'key': 'caballo_comun', 'seller': 'JugadorA', 'price': 5000, 'level': 5},
            {'key': 'corcel_de_guerra', 'seller': 'JugadorB', 'price': 20000, 'level': 20},
            {'key': 'corcel_legendario', 'seller': 'JugadorC', 'price': 100000, 'level': 70},
        ]
        y_offset = 0.15
        for offer in self.market_mounts:
            data = MOUNT_DATA[offer['key']]
            btn_text = f"{data['name']} (Vendedor: {offer['seller']}) - {offer['price']} oro"
            btn = Button(parent=self.panel, text=btn_text, y=y_offset, on_click=lambda o=offer: self.buy_mount(o))
            y_offset -= 0.12
        Button(parent=self.panel, text='Cerrar', y=-0.4, color=color.red, on_click=self.close)

    def buy_mount(self, offer):
        from data.mount_data import MOUNT_DATA
        data = MOUNT_DATA[offer['key']]
        price = offer['price']
        if self.player.gold >= price:
            self.player.gold -= price
            from inventory.inventory_manager import InventoryItem
            item = InventoryItem(item_id=offer['key'], name=data['name'], item_type='mount')
            self.player.inventory_manager.add_item(item)
            print(f"¡Has comprado {data['name']} de {offer['seller']} por {price} oro!")
        else:
            print("No tienes suficiente oro para comprar esta montura.")

    def close(self):
        destroy(self)
