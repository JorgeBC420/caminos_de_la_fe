from ursina.prefabs.grid_menu import GridMenu
from ursina import Entity

class InventoryGridMenu(GridMenu):
    def __init__(self, inventory_manager, **kwargs):
        super().__init__(**kwargs)
        self.inventory_manager = inventory_manager
        self.update_grid()

    def update_grid(self):
        self.clear()
        for item in self.inventory_manager.items:
            self.add_button(text=str(item), on_click=lambda i=item: self.equip_item(i))

    def equip_item(self, item):
        if hasattr(item, 'equip'):
            item.equip()
            print(f"Item equipado: {item}")
