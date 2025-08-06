from ursina import *
from entities.inventory import Inventory
from entities.equipment import Equipment

class AdvancedInventoryUI(Entity):
    def show_unique_item_status(self, pvp_manager, player):
        # Muestra estado de purificación, maldición y aura
        status = []
        if hasattr(player, 'unique_items') and player.unique_items:
            for item in player.unique_items:
                purif = pvp_manager.can_use_unique_item(player)
                aura = getattr(player, 'has_cursed_aura', False)
                status.append(f"{item}: {'Purificado' if purif else 'Pendiente'}" + (" (Aura visible)" if aura else ""))
        else:
            status.append("Sin ítems únicos")
        Text(parent=self.panel, text='\n'.join(status), position=(0.2, -0.3), scale=1.1)
    def __init__(self, inventory, equipment, horse=None, **kwargs):
        super().__init__(parent=camera.ui, **kwargs)
        self.inventory = inventory
        self.equipment = equipment
        self.horse = horse
        self.panel = Entity(parent=self, model='quad', scale=(1.2, 0.8), color=color.gray)
        Text(parent=self.panel, text='Inventario Avanzado', y=0.35, scale=1.5)
        self._draw_slots()
        self._draw_stats()
        self._draw_horse_preview()
        Button(parent=self.panel, text='Cerrar', position=(0.5, -0.35), color=color.red, on_click=self.close)

    def _draw_slots(self):
        slots = list(self.equipment.__dict__.keys())
        for i, slot in enumerate(slots):
            item = getattr(self.equipment, slot)
            btn = Button(parent=self.panel, text=f'{slot.capitalize()}: {item.name if item else "Vacío"}', position=(-0.5, 0.25-i*0.07), scale=(0.4,0.06))
            btn.tooltip = Tooltip(f'Efectos: {getattr(item, "effects", "Ninguno")}' if item else 'Sin efectos')

    def _draw_stats(self):
        stats = self._calculate_stats()
        y = 0.25
        for stat, value in stats.items():
            Text(parent=self.panel, text=f'{stat.capitalize()}: {value}', position=(0.2, y), scale=1.1)
            y -= 0.07

    def _draw_horse_preview(self):
        if self.horse:
            Text(parent=self.panel, text=f'Montura: {self.horse.name}', position=(0.2, -0.2), scale=1.1)
            # Aquí podrías agregar preview 3D si tienes el modelo

    def _calculate_stats(self):
        # Suma los stats de equipo y montura
        stats = {'daño': 0, 'defensa': 0, 'vida': 0, 'velocidad': 0}
        for item in self.equipment.__dict__.values():
            if item and hasattr(item, 'stats'):
                for k, v in item.stats.items():
                    stats[k] = stats.get(k, 0) + v
        if self.horse and hasattr(self.horse, 'stats'):
            for k, v in self.horse.stats.items():
                stats[k] = stats.get(k, 0) + v
        return stats

    def close(self):
        destroy(self)
