from ursina import *

class NPCDoctorUI(Entity):
    def __init__(self, player, **kwargs):
        super().__init__(parent=camera.ui, **kwargs)
        self.player = player
        self.panel = Entity(parent=self, model='quad', scale=(0.8, 0.7), color=color.cyan.tint(-.2))
        Text(parent=self.panel, text='Doctor (NPC)', y=0.3, scale=1.5)
        # Ejemplo de poción a la venta
        self.npc_potions = [
            {'name': 'Poción de Vida', 'price': 500, 'unlock_level': 1},
            {'name': 'Poción de Energía', 'price': 1200, 'unlock_level': 8},
        ]
        y_offset = 0.1
        for potion in self.npc_potions:
            btn_text = f"{potion['name']} (Nivel {potion['unlock_level']}) - {potion['price']} oro"
            Button(parent=self.panel, text=btn_text, y=y_offset, on_click=lambda p=potion: self.buy_potion(p))
            y_offset -= 0.12

    def buy_potion(self, potion):
        player_level = self.player.level
        if player_level < potion['unlock_level']:
            print(f"Necesitas ser nivel {potion['unlock_level']} para comprar esta poción.")
            return
        if self.player.gold >= potion['price']:
            self.player.gold -= potion['price']
            from inventory.inventory_manager import InventoryItem
            item = InventoryItem(item_id=potion['name'].lower().replace(' ', '_'), name=potion['name'], item_type='consumable')
            self.player.inventory_manager.add_item(item)
            print(f"¡Poción {potion['name']} comprada por {potion['price']} oro!")
        else:
            print("No tienes suficiente oro para comprar esta poción.")

    def close(self):
        destroy(self)
