from ursina import *

class NPCJewelerUI(Entity):
    def __init__(self, player, **kwargs):
        super().__init__(parent=camera.ui, **kwargs)
        self.player = player
        self.panel = Entity(parent=self, model='quad', scale=(0.8, 0.7), color=color.yellow.tint(-.3))
        Text(parent=self.panel, text='Joyero (NPC)', y=0.3, scale=1.5)
        # Ejemplo de joya a la venta
        self.npc_jewels = [
            {'name': 'Anillo de Poder', 'price': 3000, 'unlock_level': 10},
            {'name': 'Collar de Sabiduría', 'price': 7000, 'unlock_level': 20},
        ]
        y_offset = 0.1
        for jewel in self.npc_jewels:
            btn_text = f"{jewel['name']} (Nivel {jewel['unlock_level']}) - {jewel['price']} oro"
            Button(parent=self.panel, text=btn_text, y=y_offset, on_click=lambda j=jewel: self.buy_jewel(j))
            y_offset -= 0.12

    def buy_jewel(self, jewel):
        player_level = self.player.level
        if player_level < jewel['unlock_level']:
            print(f"Necesitas ser nivel {jewel['unlock_level']} para comprar esta joya.")
            return
        if self.player.gold >= jewel['price']:
            self.player.gold -= jewel['price']
            from inventory.inventory_manager import InventoryItem
            item = InventoryItem(item_id=jewel['name'].lower().replace(' ', '_'), name=jewel['name'], item_type='jewelry')
            self.player.inventory_manager.add_item(item)
            print(f"¡Joya {jewel['name']} comprada por {jewel['price']} oro!")
        else:
            print("No tienes suficiente oro para comprar esta joya.")
        Button(parent=self.panel, text='Cerrar', y=-0.4, color=color.red, on_click=self.close)

    def close(self):
        destroy(self)
