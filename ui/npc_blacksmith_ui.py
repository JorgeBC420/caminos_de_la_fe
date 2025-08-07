from ursina import *

class NPCBlacksmithUI(Entity):
    def __init__(self, player, **kwargs):
        super().__init__(parent=camera.ui, **kwargs)
        self.player = player
        self.panel = Entity(parent=self, model='quad', scale=(0.8, 0.7), color=color.gray)
        Text(parent=self.panel, text='Herrero (NPC)', y=0.3, scale=1.5)
        # Ejemplo de arma a la venta
        self.npc_weapons = [
            {'name': 'Espada de Hierro', 'price': 2000, 'unlock_level': 5},
            {'name': 'Hacha de Batalla', 'price': 6000, 'unlock_level': 15},
        ]
        y_offset = 0.1
        for weapon in self.npc_weapons:
            btn_text = f"{weapon['name']} (Nivel {weapon['unlock_level']}) - {weapon['price']} oro"
            Button(parent=self.panel, text=btn_text, y=y_offset, on_click=lambda w=weapon: self.buy_weapon(w))
            y_offset -= 0.12

    def buy_weapon(self, weapon):
        player_level = self.player.level
        if player_level < weapon['unlock_level']:
            print(f"Necesitas ser nivel {weapon['unlock_level']} para comprar esta arma.")
            return
        if self.player.gold >= weapon['price']:
            self.player.gold -= weapon['price']
            from inventory.inventory_manager import InventoryItem
            item = InventoryItem(item_id=weapon['name'].lower().replace(' ', '_'), name=weapon['name'], item_type='weapon')
            self.player.inventory_manager.add_item(item)
            print(f"¡Arma {weapon['name']} comprada por {weapon['price']} oro!")
        else:
            print("No tienes suficiente oro para comprar esta arma.")

    def close(self):
        destroy(self)
