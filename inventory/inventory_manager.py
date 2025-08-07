# Lógica para administrar ítems equipados y en mochila
from ursina import *

class InventoryItem:
    def __init__(self, item_id, name, item_type, rarity='common', stack_size=1, description="", stats_bonus=None):
        self.item_id = item_id
        self.name = name
        self.item_type = item_type  # 'weapon', 'armor', 'consumable', 'jewelry', 'material'
        self.rarity = rarity  # 'common', 'uncommon', 'rare', 'epic', 'legendary'
        self.stack_size = stack_size
        self.description = description
        self.stats_bonus = stats_bonus or {}
        self.quantity = 1
        
    def get_rarity_color(self):
        colors = {
            'common': color.white,
            'uncommon': color.green,
            'rare': color.blue,
            'epic': color.purple,
            'legendary': color.orange
        }
        return colors.get(self.rarity, color.white)
        
    def can_stack_with(self, other_item):
        return (self.item_id == other_item.item_id and 
                self.quantity + other_item.quantity <= self.stack_size)

class EquipmentSlot:
    def __init__(self, slot_type):
        self.slot_type = slot_type  # 'weapon', 'helmet', 'chest', 'legs', 'boots', 'ring', 'necklace'
        self.equipped_item = None
        
    def equip(self, item):
        if item.item_type == self.slot_type or (self.slot_type == 'weapon' and item.item_type in ['sword', 'bow', 'staff']):
            old_item = self.equipped_item
            self.equipped_item = item
            return old_item
        return None
        
    def unequip(self):
        item = self.equipped_item
        self.equipped_item = None
        return item

class InventoryManager:
    def __init__(self, player, max_slots=20):
        self.player = player
        self.max_slots = max_slots
        self.items = []  # Lista de InventoryItem
        
        # Slots de equipamiento
        self.equipment_slots = {
            'weapon': EquipmentSlot('weapon'),
            'helmet': EquipmentSlot('helmet'),
            'chest': EquipmentSlot('chest'),
            'legs': EquipmentSlot('legs'),
            'boots': EquipmentSlot('boots'),
            'ring1': EquipmentSlot('ring'),
            'ring2': EquipmentSlot('ring'),
            'necklace': EquipmentSlot('necklace'),
            'mount': EquipmentSlot('mount')  # Nuevo slot para montura
        }
        
        # Inicializar con algunos ítems básicos
        self.add_item(self.create_basic_sword())
        self.add_item(self.create_health_potion())
        
    def create_basic_sword(self):
        return InventoryItem(
            item_id='basic_sword',
            name='Espada Básica',
            item_type='weapon',
            rarity='common',
            description='Una espada simple pero efectiva',
            stats_bonus={'fuerza': 5, 'tecnica': 2}
        )
        
    def create_health_potion(self):
        return InventoryItem(
            item_id='health_potion',
            name='Poción de Vida',
            item_type='consumable',
            rarity='common',
            stack_size=10,
            description='Restaura 50 puntos de vida'
        )
        
    def add_item(self, item):
        """Añade un ítem al inventario"""
        # Intentar stackear con ítems existentes
        for existing_item in self.items:
            if existing_item.can_stack_with(item):
                existing_item.quantity += item.quantity
                print(f"Añadido {item.name} x{item.quantity} (Total: {existing_item.quantity})")
                return True
                
        # Si no se puede stackear, añadir como nuevo ítem
        if len(self.items) < self.max_slots:
            self.items.append(item)
            print(f"Añadido {item.name} al inventario")
            return True
        else:
            print("Inventario lleno!")
            return False
            
    def remove_item(self, item_id, quantity=1):
        """Remueve un ítem del inventario"""
        for item in self.items:
            if item.item_id == item_id:
                if item.quantity > quantity:
                    item.quantity -= quantity
                    print(f"Usado {item.name} x{quantity}")
                    return True
                elif item.quantity == quantity:
                    self.items.remove(item)
                    print(f"Usado {item.name} x{quantity}")
                    return True
        return False
        
    def equip_item(self, item_id):
        """Equipa un ítem del inventario. Aplica penalización si la montura es de mayor nivel que el jugador."""
        from data.mount_data import MOUNT_DATA
        item_to_equip = None
        for item in self.items:
            if item.item_id == item_id:
                item_to_equip = item
                break
        if not item_to_equip:
            print("Ítem no encontrado en el inventario")
            return False
        # Determinar slot apropiado
        slot_key = None
        penalty = 0
        if item_to_equip.item_type == 'weapon':
            slot_key = 'weapon'
        elif item_to_equip.item_type in ['helmet', 'chest', 'legs', 'boots', 'necklace']:
            slot_key = item_to_equip.item_type
        elif item_to_equip.item_type == 'ring':
            if not self.equipment_slots['ring1'].equipped_item:
                slot_key = 'ring1'
            elif not self.equipment_slots['ring2'].equipped_item:
                slot_key = 'ring2'
            else:
                slot_key = 'ring1'
        elif item_to_equip.item_type == 'mount':
            slot_key = 'mount'
            # Lógica de penalización de montura
            mount_key = item_to_equip.item_id
            if mount_key in MOUNT_DATA:
                unlock_level = MOUNT_DATA[mount_key]['unlock_level']
                player_level = self.player.level
                diff = unlock_level - player_level
                if diff > 0:
                    if diff >= 30:
                        penalty = 0.5
                    elif diff >= 20:
                        penalty = 0.3
                    elif diff >= 10:
                        penalty = 0.25
                    elif diff >= 5:
                        penalty = 0.15
                    elif diff >= 2:
                        penalty = 0.10
                self.player.mount_penalty = penalty
                if penalty > 0:
                    print(f"Penalización de efectividad: -{int(penalty*100)}% por usar montura de nivel superior.")
                else:
                    self.player.mount_penalty = 0
        if slot_key:
            slot = self.equipment_slots[slot_key]
            old_item = slot.equip(item_to_equip)
            self.items.remove(item_to_equip)
            if old_item:
                self.add_item(old_item)
            self.update_player_stats()
            print(f"Equipado: {item_to_equip.name}")
            return True
        return False
        
    def unequip_item(self, slot_key):
        """Desequipa un ítem"""
        if slot_key in self.equipment_slots:
            slot = self.equipment_slots[slot_key]
            item = slot.unequip()
            if item:
                if self.add_item(item):
                    self.update_player_stats()
                    print(f"Desequipado: {item.name}")
                    return True
                else:
                    # Si no se puede añadir al inventario, volver a equipar
                    slot.equip(item)
                    print("No hay espacio en el inventario")
                    return False
        return False
        
    def update_player_stats(self):
        """Actualiza los bonos de stats del jugador basado en el equipamiento"""
        # Resetear bonos de ítems
        self.player.stats.item_bonuses = {}
        
        # Sumar bonos de todos los ítems equipados
        for slot in self.equipment_slots.values():
            if slot.equipped_item:
                for stat, bonus in slot.equipped_item.stats_bonus.items():
                    current_bonus = self.player.stats.item_bonuses.get(stat, 0)
                    self.player.stats.item_bonuses[stat] = current_bonus + bonus
                    
        # Recalcular vida y maná máximos
        self.player.stats.max_health = self.player.stats.calculate_max_health()
        self.player.stats.max_mana = self.player.stats.calculate_max_mana()
        
        # Actualizar UI si existe
        if hasattr(self.player, 'stats_ui') and self.player.stats_ui:
            self.player.stats_ui.update_ui()
            
    def use_consumable(self, item_id):
        """Usa un consumible"""
        for item in self.items:
            if item.item_id == item_id and item.item_type == 'consumable':
                if self.apply_consumable_effect(item):
                    self.remove_item(item_id, 1)
                    return True
        return False
        
    def apply_consumable_effect(self, item):
        """Aplica el efecto de un consumible"""
        if item.item_id == 'health_potion':
            if self.player.health < self.player.max_health:
                heal_amount = min(50, self.player.max_health - self.player.health)
                self.player.health += heal_amount
                print(f"Vida restaurada: +{heal_amount}")
                return True
            else:
                print("Ya tienes la vida completa")
                return False
        # Añadir más efectos de consumibles aquí
        return False
        
    def get_equipped_items(self):
        """Retorna una lista de ítems equipados"""
        equipped = {}
        for slot_name, slot in self.equipment_slots.items():
            if slot.equipped_item:
                equipped[slot_name] = slot.equipped_item
        return equipped
        
    def get_total_stats_bonus(self):
        """Retorna el bono total de stats del equipamiento"""
        return self.player.stats.item_bonuses.copy()
        
    def print_inventory(self):
        """Imprime el contenido del inventario (para debugging)"""
        print("\n=== INVENTARIO ===")
        for i, item in enumerate(self.items):
            rarity_symbol = {'common': '', 'uncommon': '★', 'rare': '★★', 'epic': '★★★', 'legendary': '★★★★'}
            symbol = rarity_symbol.get(item.rarity, '')
            if item.quantity > 1:
                print(f"{i+1}. {item.name} x{item.quantity} {symbol}")
            else:
                print(f"{i+1}. {item.name} {symbol}")
                
        print("\n=== EQUIPAMIENTO ===")
        for slot_name, slot in self.equipment_slots.items():
            if slot.equipped_item:
                print(f"{slot_name.capitalize()}: {slot.equipped_item.name}")
            else:
                print(f"{slot_name.capitalize()}: (vacío)")
        print("==================\n")
