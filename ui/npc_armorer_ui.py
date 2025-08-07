from ursina import *

class NPCArmorerUI(Entity):
    def __init__(self, player, **kwargs):
        super().__init__(parent=camera.ui, **kwargs)
        self.player = player
        self.panel = Entity(parent=self, model='quad', scale=(0.8, 0.7), color=color.gray.tint(-.1))
        Text(parent=self.panel, text='Armero (NPC)', y=0.3, scale=1.5)
        # Ejemplo de armadura a la venta
        self.npc_armors = [
            {'name': 'Armadura de Cuero', 'price': 1500, 'unlock_level': 3},
            {'name': 'Armadura de Placas', 'price': 8000, 'unlock_level': 18},
        ]
        y_offset = 0.1
        for armor in self.npc_armors:
            btn_text = f"{armor['name']} (Nivel {armor['unlock_level']}) - {armor['price']} oro"
            Button(parent=self.panel, text=btn_text, y=y_offset, on_click=lambda a=armor: self.buy_armor(a))
            y_offset -= 0.12

    def buy_armor(self, armor):
        player_level = self.player.level
        if player_level < armor['unlock_level']:
            print(f"Necesitas ser nivel {armor['unlock_level']} para comprar esta armadura.")
            return
        if self.player.gold >= armor['price']:
            self.player.gold -= armor['price']
            from inventory.inventory_manager import InventoryItem
            item = InventoryItem(item_id=armor['name'].lower().replace(' ', '_'), name=armor['name'], item_type='armor')
            self.player.inventory_manager.add_item(item)
            print(f"¡Armadura {armor['name']} comprada por {armor['price']} oro!")
        else:
            print("No tienes suficiente oro para comprar esta armadura.")

    def close(self):
        destroy(self)
