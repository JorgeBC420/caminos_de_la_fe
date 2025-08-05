# from ursina import *
from ursina import Entity, Button, color
# Interfaz arrastrable de inventario y lógica de equipamiento

class InventoryUI(Entity):
    def __init__(self, inventory_manager, **kwargs):
        super().__init__(**kwargs)
        self.inventory_manager = inventory_manager
        self.slots = []
        self.create_slots()

    def create_slots(self):
        for i in range(self.inventory_manager.size):
            slot = Button(parent=self, position=(i*0.2,0), color=color.white, draggable=True)
            slot.slot_index = i
            slot.on_drop = self.on_drop
            self.slots.append(slot)

    def on_drop(self, dropped_item):
        # Lógica para equipar el item si es equipable
        if hasattr(dropped_item, 'equip'):
            dropped_item.equip()
            print(f"Item equipado: {dropped_item}")
        else:
            print(f"Item soltado en slot: {dropped_item}")
# inventory_ui.py - Parte del módulo ui
