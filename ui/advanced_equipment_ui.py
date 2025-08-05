from ursina import *

class EquipmentUIPanel(Entity):
    def __init__(self, player, **kwargs):
        super().__init__(parent=camera.ui, **kwargs)
        self.player = player
        self.player_stats = player.stats
        self.inventory_manager = player.inventory_manager

        self.bg = Entity(parent=self, model='quad', color=color.black66, scale=(1.3, 0.9))

        self.left_panel = Entity(parent=self, position=(-0.55, 0), scale=(0.5, 0.8))
        self.right_panel = Entity(parent=self, position=(0.35, 0), scale=(0.5, 0.8))

        self.create_equipment_slots()
        self.create_stat_display()
        self.update_equipment_slots()
        self.update_stats()
        self.update_skills()

    def update_skills(self):
        # Muestra las habilidades disponibles según la facción del jugador
        if hasattr(self, 'player'):
            skills = self.player.get_available_skills()
            self.skill_buttons = []
            for i, skill in enumerate(skills):
                btn = Button(text=skill['name'], position=(0.5, 0.4-i*0.08), scale=(0.18,0.06), color=color.azure, parent=self)
                btn.on_click = lambda s=skill: self.player.use_skill_by_name(s['name'])
                self.skill_buttons.append(btn)

    def create_equipment_slots(self):
        self.equipment_labels = {}
        slots = ['weapon', 'helmet', 'chest', 'legs', 'boots', 'ring1', 'ring2', 'necklace']
        slot_names = {
            'weapon': 'Arma', 'helmet': 'Casco', 'chest': 'Armadura', 'legs': 'Piernas',
            'boots': 'Botas', 'ring1': 'Anillo 1', 'ring2': 'Anillo 2', 'necklace': 'Joyería'
        }
        for i, slot in enumerate(slots):
            y = 0.35 - i * 0.1
            Text(slot_names[slot] + ':', parent=self.left_panel, position=(-0.4, y), origin=(-0.5, 0))
            self.equipment_labels[slot] = Text('Ninguno', parent=self.left_panel, position=(-0.1, y), origin=(-0.5, 0))

    def update_equipment_slots(self):
        equipped = self.inventory_manager.get_equipped_items()
        for slot, label in self.equipment_labels.items():
            item = equipped.get(slot)
            label.text = item.name if item else 'Ninguno'

    def create_stat_display(self):
        self.stat_labels = {}
        stats = self.get_stats_summary()
        for i, (k, v) in enumerate(stats.items()):
            y = 0.35 - i * 0.05
            Text(k + ':', parent=self.right_panel, position=(-0.4, y), origin=(-0.5, 0))
            self.stat_labels[k] = Text(str(v), parent=self.right_panel, position=(0, y), origin=(-0.5, 0))

    def get_stats_summary(self):
        # Combina stats base y bonus de equipo
        stats = self.player_stats.stats.copy()
        for stat, bonus in self.inventory_manager.get_total_stats_bonus().items():
            stats[stat] = stats.get(stat, 0) + bonus
        stats['max_health'] = self.player_stats.max_health
        stats['max_mana'] = self.player_stats.max_mana
        return stats

    def update_stats(self):
        stats = self.get_stats_summary()
        for k, label in self.stat_labels.items():
            label.text = str(stats.get(k, 0))
        self.update_equipment_slots()
