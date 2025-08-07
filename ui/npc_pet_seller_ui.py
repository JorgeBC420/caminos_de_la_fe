from ursina import *
from data.pet_data import PET_DATA

class NPCPetSellerUI(Entity):
    def __init__(self, player, **kwargs):
        super().__init__(parent=camera.ui, **kwargs)
        self.player = player
        self.panel = Entity(parent=self, model='quad', scale=(0.8, 0.7), color=color.lime.tint(-.2))
        Text(parent=self.panel, text='Vendedor de Mascotas (NPC)', y=0.3, scale=1.5)
        # Ejemplo de mascota a la venta
        from data.pet_data import PET_DATA
        self.npc_pets = [
            {'key': 'gato', 'price': 2000},
            {'key': 'perro', 'price': 3500},
        ]
        y_offset = 0.1
        for offer in self.npc_pets:
            data = PET_DATA[offer['key']]
            btn_text = f"{data['name']} (Nivel {data['unlock_level']}) - {offer['price']} oro"
            Button(parent=self.panel, text=btn_text, y=y_offset, on_click=lambda o=offer: self.buy_pet(o))
            y_offset -= 0.12

    def buy_pet(self, offer):
        from data.pet_data import PET_DATA
        data = PET_DATA[offer['key']]
        player_level = self.player.level
        unlock_level = data['unlock_level']
        price = offer['price']
        if player_level < unlock_level:
            print(f"Necesitas ser nivel {unlock_level} para comprar esta mascota.")
            return
        if self.player.gold >= price:
            self.player.gold -= price
            from inventory.inventory_manager import InventoryItem
            item = InventoryItem(item_id=offer['key'], name=data['name'], item_type='pet')
            self.player.inventory_manager.add_item(item)
            print(f"¡Mascota {data['name']} comprada por {price} oro!")
        else:
            print("No tienes suficiente oro para comprar esta mascota.")
        Button(parent=self.panel, text='Cerrar', y=-0.4, color=color.red, on_click=self.close)

    def close(self):
        destroy(self)
