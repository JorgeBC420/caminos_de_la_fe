from ursina import *

# --- Lógica de estadísticas del jugador ---
class PlayerStats:
    def __init__(self, base_stats=None, item_bonuses=None, horse_bonuses=None):
        default_stats = {
            'nivel': 1,
            'fuerza': 10,
            'tecnica': 10,
            'destreza': 10,
            'defensa': 10,
            'resistencia': 10,
            'velocidad': 10,
            'agilidad': 10,
            'inteligencia': 10,
        }
        self.stats = base_stats or default_stats.copy()
        self.item_bonuses = item_bonuses or {}   # Ejemplo: {'fuerza': 2, 'defensa': 1}
        self.horse_bonuses = horse_bonuses or {} # Ejemplo: {'fuerza': 1, 'velocidad': 3}
        self.max_health = self.calculate_max_health()
        self.max_mana = self.calculate_max_mana()

    def get_total_stat(self, stat_name):
        base = self.stats.get(stat_name, 0)
        item = self.item_bonuses.get(stat_name, 0)
        horse = self.horse_bonuses.get(stat_name, 0)
        return base + item + horse

    def get_bonus(self, stat_name):
        item = self.item_bonuses.get(stat_name, 0)
        horse = self.horse_bonuses.get(stat_name, 0)
        return item + horse

    def calculate_max_health(self):
        return 100 + self.stats['nivel'] * 20 + self.get_total_stat('resistencia') * 5

    def calculate_max_mana(self):
        return 50 + self.stats['nivel'] * 10 + self.get_total_stat('inteligencia') * 3

    def improve_stat(self, stat_name, amount=1):
        if stat_name in self.stats:
            cost = (self.stats[stat_name] + 1) ** 2
            if hasattr(self, 'gold') and self.gold < cost:
                print(f"No tienes suficiente oro para mejorar {stat_name}. Costo: {cost}")
                return False
            self.stats[stat_name] += amount
            if hasattr(self, 'gold'):
                self.gold -= cost
            if stat_name in ['nivel', 'resistencia', 'inteligencia']:
                self.max_health = self.calculate_max_health()
                self.max_mana = self.calculate_max_mana()
            print(f"Mejoraste {stat_name} a {self.stats[stat_name]}. Oro restante: {getattr(self, 'gold', 0)}")
            return True
        return False

# --- UI de estadísticas del jugador ---
class PlayerStatsUI(Entity):
    def __init__(self, player, **kwargs):
        super().__init__(parent=camera.ui, scale=1, **kwargs)
        self.player = player
        self.stats = player.stats  # Instancia de PlayerStats
        self.gold = player.gold    # Oro actual del jugador
        self.stat_cost = 50        # Coste por mejorar cada stat

        self.text_elements = {}
        self.buttons = {}

        self.selected_abilities = []  # Habilidades básicas seleccionadas
        self.ability_buttons = {}
        self.ultimate_label = None
        self.create_ui()

    def create_ui(self):
        bg = Entity(parent=self, model='quad', scale=(0.6, 1.0), color=color.black66, position=(0, 0))
        title = Text("Estadísticas del Personaje", parent=self, position=(-0.2, 0.45), scale=1.5)

        # --- Stats ---
        y_start = 0.35
        for i, stat in enumerate(self.stats.stats.keys()):
            y = y_start - i * 0.06
            base = self.stats.stats.get(stat, 0)
            bonus = self.stats.get_bonus(stat)
            cost = (base + 1) ** 2
            if bonus > 0:
                label_text = f"{stat.capitalize()}: {base + bonus} (+{bonus})"
            else:
                label_text = f"{stat.capitalize()}: {base}"
            label = Text(
                text=label_text,
                parent=self,
                position=(-0.2, y),
                scale=0.9
            )
            self.text_elements[stat] = label

            can_afford = self.gold >= cost
            btn = Button(
                text=f"+ ({cost})",
                parent=self,
                position=(0.15, y),
                scale=(0.13, 0.05),
                color=color.red if not can_afford else color.azure,
                text_color=color.white,
                on_click=lambda s=stat: self.increase_stat(s),
                enabled=can_afford
            )
            self.buttons[stat] = btn

        # --- Salud, maná y oro ---
        self.hp_text = Text(
            text=f"Vida Máx: {self.stats.max_health}",
            parent=self,
            position=(-0.2, -0.25),
            scale=0.9
        )
        self.mp_text = Text(
            text=f"Maná Máx: {self.stats.max_mana}",
            parent=self,
            position=(-0.2, -0.32),
            scale=0.9
        )
        self.gold_text = Text(
            text=f"Oro: {self.gold}",
            parent=self,
            position=(-0.2, -0.39),
            scale=0.9
        )

        # --- Habilidades básicas (selección de 2 de 3) ---
        ability_y = -0.05
        faction = getattr(self.player, 'faction', None)
        abilities = []
        if faction and hasattr(faction, 'abilities'):
            abilities = list(faction.abilities.values())
        # Si no hay facción, usar ejemplo
        if not abilities:
            abilities = ['Habilidad 1', 'Habilidad 2', 'Habilidad 3']
        Text("Selecciona 2 habilidades básicas:", parent=self, position=(-0.2, ability_y), scale=1.1)
        for i, ab in enumerate(abilities):
            ay = ability_y - (i+1)*0.06
            btn = Button(
                text=ab,
                parent=self,
                position=(0.0, ay),
                scale=(0.22, 0.05),
                color=color.azure if ab in self.selected_abilities else color.gray,
                text_color=color.white,
                on_click=lambda a=ab: self.toggle_ability(a)
            )
            self.ability_buttons[ab] = btn

        # --- Ultimate ---
        ultimate = getattr(faction, 'ultimate', 'Ultimate') if faction else 'Ultimate'
        self.ultimate_label = Text(
            text=f"Ultimate: {ultimate}",
            parent=self,
            position=(-0.2, -0.28),
            scale=1.1,
            color=color.gold
        )

    def update_ui(self):
        for stat, label in self.text_elements.items():
            base = self.stats.stats.get(stat, 0)
            bonus = self.stats.get_bonus(stat)
            cost = (base + 1) ** 2
            if bonus > 0:
                label.text = f"{stat.capitalize()}: {base + bonus} (+{bonus})"
            else:
                label.text = f"{stat.capitalize()}: {base}"
            btn = self.buttons[stat]
            btn.text = f"+ ({cost})"
            can_afford = self.gold >= cost
            btn.color = color.red if not can_afford else color.azure
            btn.enabled = can_afford
        self.hp_text.text = f"Vida Máx: {self.stats.max_health}"
        self.mp_text.text = f"Maná Máx: {self.stats.max_mana}"
        self.gold_text.text = f"Oro: {self.gold}"
        # Actualiza botones de habilidades
        for ab, btn in self.ability_buttons.items():
            btn.color = color.azure if ab in self.selected_abilities else color.gray
            btn.enabled = (ab in self.selected_abilities or len(self.selected_abilities) < 2)
        # Ultimate
        if self.ultimate_label:
            faction = getattr(self.player, 'faction', None)
            ultimate = getattr(faction, 'ultimate', 'Ultimate') if faction else 'Ultimate'
            self.ultimate_label.text = f"Ultimate: {ultimate}"

    def increase_stat(self, stat_name):
        current_value = self.stats.stats.get(stat_name, 0)
        cost = (current_value + 1) ** 2
        if self.gold >= cost:
            if self.stats.improve_stat(stat_name):
                self.gold -= cost
            self.update_ui()
        else:
            print(f"No tienes suficiente oro para mejorar {stat_name}. Costo requerido: {cost}")

    def toggle_ability(self, ability_name):
        if ability_name in self.selected_abilities:
            self.selected_abilities.remove(ability_name)
        elif len(self.selected_abilities) < 2:
            self.selected_abilities.append(ability_name)
        self.update_ui()

# NOTAS:
# - Cuando crees la lógica de ítems, actualiza item_bonuses en PlayerStats.
# - Cuando crees la lógica de caballo, actualiza horse_bonuses en PlayerStats.
# - La UI ya está preparada para mostrar los bonus automáticamente.