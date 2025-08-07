from ursina import *
from datetime import datetime
from data.factions import FACTIONS
from data.config import GameConfig
from systems.auto_combat import AutoCombatSystem
from systems.faction_war import FactionWarClient
from entities.enemy import Enemy
from systems.stats import PlayerStats
from systems.stats import PlayerStatsUI
from utils.camera_controller import ThirdPersonCamera
from data.faction_advantages import FACTION_ADVANTAGES
from systems.progression import get_upgrade_cost
from items.legendary.legendary_item import LegendaryItem
from systems.siege import simulate_pvp
from systems.monetization import FaithPass
from systems.events import EventSystem
from api.client import APIClient
import math
import random
from ursina import invoke, Entity, color

faction_war_client = FactionWarClient("https://tujuego.com/api")

def create_test_enemy(position=(5,0,5)):
    from ursina import Entity, color, Vec3
    enemy = Entity(model='cube', color=color.red, position=position, scale=(1,2,1))
    enemy.health = 100
    enemy.defense = 8
    enemy.mass = 70
    enemy.velocity = Vec3(0,0,0)
    return enemy

def create_test_object(position=(2,0,2)):
    from ursina import Entity, color
    obj = Entity(model='sphere', color=color.green, position=position, scale=0.7)
    def on_pickup(player):
        print(f"Objeto recogido por {player}")
        obj.enabled = False
    obj.on_pickup = on_pickup
    return obj

# Added mount management system
from systems.mount_manager import MountManager

class Player(Entity):
    def add_fragment(self, fragment_name, amount=1):
        """Agrega fragmentos al inventario del jugador."""
        if not hasattr(self, 'fragments'):
            self.fragments = {}
        if fragment_name in self.fragments:
            self.fragments[fragment_name] += amount
        else:
            self.fragments[fragment_name] = amount
        print(f"Fragmento '{fragment_name}' agregado. Total: {self.fragments[fragment_name]}")

    def complete_epic_mission(self, mission):
        """Otorga el fragmento de recompensa al completar una misión épica."""
        reward = mission.get('reward')
        if reward and 'Fragmento' in reward:
            self.add_fragment(reward)
        # Aquí se puede agregar lógica para recompensas legendarias, oro, etc.
    def get_available_skills(self):
        """Devuelve las habilidades básicas y secundarias disponibles para la UI según la facción"""
        if self.faction.name == 'Egipcios':
            return [
                {'name': 'Espina de Escorpión', 'method': self.scorpion_sting},
                {'name': 'Arena Sanadora', 'method': self.healing_sand},
                {'name': 'Bendición Solar', 'method': self.solar_blessing}
            ]
        elif self.faction.name == 'Romanos':
            return [
                {'name': 'Jabalina Imperial', 'method': self.imperial_javelin},
                {'name': 'Embate de Scutum', 'method': self.scutum_bash},
                {'name': 'Coraje de la Legión', 'method': self.legion_courage}
            ]
        elif self.faction.name == 'Vikingos':
            return [
                {'name': 'Hacha Errante', 'method': self.wandering_axe},
                {'name': 'Rugido del Lobo', 'method': self.wolf_roar},
                {'name': 'Embestida de Escudo', 'method': self.shield_charge}
            ]
        elif self.faction.name == 'Griegos':
            return [
                {'name': 'Flecha Reluciente', 'method': self.shining_arrow},
                {'name': 'Toque de Apolo', 'method': self.apollo_touch},
                {'name': 'Furia de Ares', 'method': self.ares_fury}
            ]
        # ...agrega otras facciones si es necesario...
        return []

    def use_skill_by_name(self, skill_name):
        """Permite a la UI activar una habilidad por nombre"""
        for skill in self.get_available_skills():
            if skill['name'] == skill_name:
                skill['method']()
                return True
        print(f"Habilidad '{skill_name}' no encontrada para la facción {self.faction.name}")
        return False
    def apply_physics_to_enemy(self, enemy):
        # Aplica impacto y daño físico al enemigo
        if hasattr(enemy, 'health'):
            damage = self.attack_damage - getattr(enemy, 'defense', 0)
            damage = max(damage, 1)
            enemy.health -= damage
            print(f"Impacto: {self.impact}, Daño infligido: {damage}")
            # Aplica retroceso físico si el enemigo tiene masa y velocidad
            if hasattr(enemy, 'mass') and hasattr(enemy, 'velocity'):
                force = self.impact * self.mass / (enemy.mass + 1)
                enemy.velocity += Vec3(force, 0, force)

    def check_collision_with_object(self, obj):
        # Colisión simple: si la distancia es menor a cierto umbral
        if hasattr(obj, 'position'):
            dist = (self.position - obj.position).length()
            if dist < 1.0:
                print(f"Colisión con objeto: {obj}")
                # Ejemplo: recoger objeto, activar evento, etc.
                if hasattr(obj, 'on_pickup'):
                    obj.on_pickup(self)
    def update(self):
        # Movimiento influenciado por velocidad y agilidad
        move_speed = self.stats.stats.get('velocidad', 10) * 0.1 + self.stats.stats.get('agilidad', 10) * 0.05
        direction = Vec3(0, 0, 0)
        if self.joystick and hasattr(self.joystick, 'value'):
            direction = Vec3(self.joystick.value.x, 0, self.joystick.value.y).normalized()
        self.velocity.x = direction.x * move_speed
        self.velocity.z = direction.z * move_speed

        # Gravedad y salto
        if not self.is_on_ground:
            self.velocity.y += self.gravity * time.dt
        else:
            self.velocity.y = 0

        # Aplicar movimiento
        self.position += self.velocity * time.dt

        # Impacto y daño físico
        self.impact = self.stats.stats.get('fuerza', 10) * 0.2
        self.attack_damage = self.stats.stats.get('fuerza', 10) * 1.5 + self.stats.stats.get('tecnica', 10) * 0.5

        # Defensa y resistencia a impactos
        self.defense = self.stats.stats.get('defensa', 10) * 1.2 + self.stats.stats.get('resistencia', 10) * 0.8

        # Precisión y habilidades especiales
        self.precision = self.stats.stats.get('destreza', 10) * 0.7 + self.stats.stats.get('tecnica', 10) * 0.6

        # Vida máxima y aguante
        self.max_health = 100 + self.stats.stats.get('resistencia', 10) * 5

        # Maná y habilidades mágicas
        self.max_mana = 50 + self.stats.stats.get('inteligencia', 10) * 3

        # Colisiones simples (ejemplo)
        if self.position.y < 0:
            self.position.y = 0
            self.is_on_ground = True
        else:
            self.is_on_ground = False
    def __init__(self, faction_name='Cruzados', build=None, joystick=None, **kwargs):
        super().__init__(**kwargs)
        from data.basic_abilities import BASIC_ABILITIES
        from data.ultimate_abilities import ULTIMATE_ABILITIES
        self.faction = FACTIONS[faction_name]
        try:
            self.model = load_model('Soldado CRUZADO.fbx')
        except Exception as e:
            print(f"Error al cargar modelo Soldado CRUZADO.fbx: {e}")
            self.model = 'cube'
        self.color = self.faction.color
        self.collider = 'box'
        self.scale = (1, 2, 1)
        self.speed = GameConfig.PLAYER_SPEED
        self.health = GameConfig.PLAYER_HEALTH
        self.max_health = GameConfig.PLAYER_HEALTH
        self.attack_damage = GameConfig.PLAYER_DAMAGE
        self.joystick = joystick if joystick is not None else self.create_virtual_joystick()
        self.mass = 80
        self.gravity = -9.8
        self.force = Vec3(0, 0, 0)
        self.velocity = Vec3(0, 0, 0)
        self.impact = 0
        self.is_on_ground = True
        self.mp = getattr(self, 'mana', 100)
        self.abilities = {}
        # Registrar solo las habilidades seleccionadas del build
        if build:
            for ab in BASIC_ABILITIES.get(faction_name, []):
                if ab['key'] in build['basics']:
                    self.abilities[ab['key']] = {**ab, 'ready': True}
            ult = ULTIMATE_ABILITIES.get(faction_name)
            if ult and ult['key'] == build['ultimate']:
                self.abilities[ult['key']] = {**ult, 'ready': True}
        # --- Sistema avanzado de niveles y XP ---
        # --- Centralización de experiencia y nivel ---
        self.stats = PlayerStats()
        self.exp_system = ExperienceSystem(self)

        # --- Sistema de cámara en tercera persona ---
        self.camera_controller = ThirdPersonCamera(self)

        # --- UI de estadísticas (opcional: solo si quieres mostrarla al crear el jugador) ---
        # self.stats_ui = PlayerStatsUI(self)

        # --- Habilidades ---
        self.abilities = {
            'basic_attack': {'cooldown': 0.8, 'ready': True},
            'ability1': {'cooldown': 5, 'ready': True},
            'ability2': {'cooldown': 8, 'ready': True},
            'ultimate': {'cooldown': 30, 'ready': True}
        }


        # --- Integración con sistemas externos ---
        self.auto_combat = AutoCombatSystem(self)
        self.faction_war_contribution = 0
        self.last_contribution_date = None
        self.auth_token = "example_token"
        
        # --- Sistemas de progresión ---
        from systems.progression import ExperienceSystem, QuestSystem, DailyRewardSystem
        from inventory.inventory_manager import InventoryManager
        
        self.exp_system = ExperienceSystem(self)
        self.quest_system = QuestSystem(self)
        self.daily_rewards = DailyRewardSystem(self)
        self.inventory_manager = InventoryManager(self)

        # Added mount management system
        self.mount_manager = MountManager(self)
        self.active_mount_key = 'corcel_de_guerra_aethelgardia'
        self.state = 'walking'

    def create_virtual_joystick(self):
        # Polígono simple para pruebas de joystick
        from ui.virtual_joystick import VirtualJoystick
        return VirtualJoystick(parent=self)

    @property
    def level(self):
        return self.exp_system.level

    @level.setter
    def level(self, value):
        self.exp_system.level = value

    @property
    def experience(self):
        return self.exp_system.experience

    @experience.setter
    def experience(self, value):
        self.exp_system.experience = value

    @property
    def experience_to_next_level(self):
        return self.exp_system.calculate_required_xp(self.level)

    def add_experience(self, amount, source="mission"):
        self.exp_system.add_experience(amount, source)

    def save_data(self):
        self.exp_system.save_data()

    def load_data(self):
        self.exp_system.load_data()

    @property
    def level(self):
        return self._level

    @level.setter
    def level(self, value):
        self._level = value

    @property
    def experience(self):
        return self._experience

    @experience.setter
    def experience(self, value):
        self._experience = value

    @property
    def experience_to_next_level(self):
        return 100 * self.level

    def add_experience(self, amount):
        self.experience += amount
        print(f"Ganaste {amount} XP. Total: {self.experience}")
        if self.experience >= self.experience_to_next_level:
            self.level_up()

    def level_up(self):
        self.level += 1
        self.experience = 0
        print(f"¡Subiste a nivel {self.level}!")
        
    def update(self):
        if self.state == 'mounted':
            direction = Vec3(0, 0, 0)
            if self.joystick and hasattr(self.joystick, 'value'):
                direction = Vec3(self.joystick.value.x, 0, self.joystick.value.y).normalized()
            self.mount_manager.active_mount_instance.position += direction * self.mount_manager.active_mount_instance.speed * time.dt
            if direction.length() > 0:
                self.mount_manager.active_mount_instance.look_at(self.mount_manager.active_mount_instance.position + direction)
        else:
            # Movimiento influenciado por velocidad y agilidad
            move_speed = self.stats.stats.get('velocidad', 10) * 0.1 + self.stats.stats.get('agilidad', 10) * 0.05
            direction = Vec3(0, 0, 0)
            if self.joystick and hasattr(self.joystick, 'value'):
                direction = Vec3(self.joystick.value.x, 0, self.joystick.value.y).normalized()
            self.velocity.x = direction.x * move_speed
            self.velocity.z = direction.z * move_speed

            # Gravedad y salto
            if not self.is_on_ground:
                self.velocity.y += self.gravity * time.dt
            else:
                self.velocity.y = 0

            # Aplicar movimiento
            self.position += self.velocity * time.dt

            # Impacto y daño físico
            self.impact = self.stats.stats.get('fuerza', 10) * 0.2
            self.attack_damage = self.stats.stats.get('fuerza', 10) * 1.5 + self.stats.stats.get('tecnica', 10) * 0.5

            # Defensa y resistencia a impactos
            self.defense = self.stats.stats.get('defensa', 10) * 1.2 + self.stats.stats.get('resistencia', 10) * 0.8

            # Precisión y habilidades especiales
            self.precision = self.stats.stats.get('destreza', 10) * 0.7 + self.stats.stats.get('tecnica', 10) * 0.6

            # Vida máxima y aguante
            self.max_health = 100 + self.stats.stats.get('resistencia', 10) * 5

            # Maná y habilidades mágicas
            self.max_mana = 50 + self.stats.stats.get('inteligencia', 10) * 3

            # Colisiones simples (ejemplo)
            if self.position.y < 0:
                self.position.y = 0
                self.is_on_ground = True
            else:
                self.is_on_ground = False
    def input(self, key):
        if key == 'm':
            if self.state == 'mounted':
                self.mount_manager.dismount_player()
            elif self.state == 'walking':
                self.mount_manager.summon_mount(self.active_mount_key)
        if key == 'left mouse down':
            if mouse.x > -0.3:
                if self.can_attack:
                    self.attack()
                    
        # Mostrar/ocultar la UI de stats con TAB
        if key == 'tab':
            if not hasattr(self, 'stats_ui') or self.stats_ui is None:
                self.stats_ui = PlayerStatsUI(self)
            else:
                self.stats_ui.enabled = not self.stats_ui.enabled
                
        # Habilidades con teclas numéricas
        if key == '1':
            self.use_ability('basic_attack')
        elif key == '2':
            self.use_ability('ability1')
        elif key == '3':
            self.use_ability('ability2')
        elif key == '4':
            self.use_ability('ultimate')
            
        # Teclas de sistemas adicionales
        elif key == 'i':
            self.inventory_manager.print_inventory()
        elif key == 'q':
            self.print_quest_status()
        elif key == 'r':
            self.daily_rewards.claim_daily_reward()
        elif key == 'h':
            self.inventory_manager.use_consumable('health_potion')

    def print_quest_status(self):
        """Imprime el estado de las misiones"""
        print("\n=== MISIONES ACTIVAS ===")
        if not self.quest_system.active_quests:
            print("No hay misiones activas")
        else:
            for quest in self.quest_system.active_quests:
                print(f"{quest['name']}: {quest['progress']}/{quest['target']}")
        
        print("\n=== MISIONES DISPONIBLES ===")
        if not self.quest_system.available_quests:
            print("No hay misiones disponibles")
        else:
            for i, quest in enumerate(self.quest_system.available_quests):
                print(f"{i+1}. {quest['name']}: {quest['description']}")
        print("==========================\n")
    
    def print_daily_rewards_status(self):
        """Mostrar recompensas diarias"""
        print("\n=== RECOMPENSAS DIARIAS ===")
        print(f"Días consecutivos: {self.daily_rewards.consecutive_days}")
        if self.daily_rewards.can_claim_daily():
            print("¡Recompensa diaria disponible! Presiona R para reclamar")
        else:
            print("Ya has reclamado tu recompensa diaria")
        print("===========================\n")

    def use_ability(self, key):
        data = self.abilities.get(key)
        if not data or not data['ready'] or self.mp < data['cost_mp']:
            print(f"No puedes usar {key}: cooldown o maná insuficiente.")
            return
        self.mp -= data['cost_mp']
        data['ready'] = False
        from ursina import invoke
        invoke(setattr, data, 'ready', True, delay=data['cd'])
        self.ultimate_charge = getattr(self, 'ultimate_charge', 0) + data.get('ult_charge', 0)
        print(f"Usaste {data['name']} (key={key})")
        # Aquí ejecutas el efecto real: daño, curas, control...
        try:
            from systems.combat import CombatSystem
            CombatSystem.execute(self, key)
        except Exception as e:
            print(f"No se pudo ejecutar efecto de {key}: {e}")
                
    def faction_ability_1(self):
        """Habilidad específica de facción 1"""
        if self.faction.name == 'Cruzados':
            self.crusader_shield()
        elif self.faction.name == 'Sarracenos':
            self.archer_volley()
        elif self.faction.name == 'Antiguos':
            self.ancient_knowledge()
        elif self.faction.name == 'Egipcios':
            self.scorpion_sting()
        elif self.faction.name == 'Romanos':
            self.imperial_javelin()
        elif self.faction.name == 'Vikingos':
            self.wandering_axe()
        elif self.faction.name == 'Griegos':
            self.shining_arrow()
            
    def faction_ability_2(self):
        """Habilidad específica de facción 2"""
        if self.faction.name == 'Cruzados':
            self.divine_strike()
        elif self.faction.name == 'Sarracenos':
            self.swift_movement()
        elif self.faction.name == 'Antiguos':
            self.arcane_blast()
        elif self.faction.name == 'Egipcios':
            self.healing_sand()
        elif self.faction.name == 'Romanos':
            self.scutum_bash()
        elif self.faction.name == 'Vikingos':
            self.wolf_roar()
        elif self.faction.name == 'Griegos':
            self.apollo_touch()
    # --- Habilidades básicas y secundarias Egipcios ---
    def scorpion_sting(self):
        """Espina de Escorpión: Veneno lento"""
        if self.mana < 20:
            print("No tienes suficiente maná.")
            return
        self.mana -= 20
        target = self.get_enemies(radius=6)[0] if self.get_enemies(radius=6) else None
        if target:
            target.apply_debuff('veneno_lento', duration=4, tick=lambda e: e.take_damage(int(e.health * 0.03)))
            print("Espina de Escorpión: Veneno lento aplicado")
            self.charge_ultimate(5)

    def healing_sand(self):
        """Arena Sanadora: Cura en área"""
        if self.mana < 18:
            print("No tienes suficiente maná.")
            return
        self.mana -= 18
        for ally in self.get_allies(radius=6):
            ally.health = min(ally.max_health, ally.health + int(ally.max_health * 0.08))
        print("Arena Sanadora: Curación aplicada")
        self.charge_ultimate(4)

    def solar_blessing(self):
        """Bendición Solar: Buff de daño"""
        if self.mana < 25:
            print("No tienes suficiente maná.")
            return
        self.mana -= 25
        target = self  # Puede ser a sí mismo o a un aliado
        target.attack_damage *= 1.1
        print("Bendición Solar: +10% daño")
        self.charge_ultimate(6)
        invoke(lambda: setattr(target, 'attack_damage', target.attack_damage / 1.1), delay=5)

    # --- Habilidades básicas y secundarias Romanos ---
    def imperial_javelin(self):
        """Jabalina Imperial: Daño directo"""
        if self.mana < 22:
            print("No tienes suficiente maná.")
            return
        self.mana -= 22
        target = self.get_enemies(radius=6)[0] if self.get_enemies(radius=6) else None
        if target:
            damage = int(target.max_health * 0.12)
            target.take_damage(damage)
            print(f"Jabalina Imperial: {damage} daño directo")
            self.charge_ultimate(5)

    def scutum_bash(self):
        """Embate de Scutum: Aturde y sangra"""
        if self.mana < 18:
            print("No tienes suficiente maná.")
            return
        self.mana -= 18
        target = self.get_enemies(radius=4)[0] if self.get_enemies(radius=4) else None
        if target:
            target.apply_debuff('aturdimiento', duration=0.5)
            target.apply_debuff('sangrado_leve', duration=3, tick=lambda e: e.take_damage(int(e.health * 0.02)))
            print("Embate de Scutum: Aturdimiento y sangrado leve aplicado")
            self.charge_ultimate(4)

    def legion_courage(self):
        """Coraje de la Legión: Buff de defensa"""
        if self.mana < 20:
            print("No tienes suficiente maná.")
            return
        self.mana -= 20
        for ally in self.get_allies(radius=6):
            ally.defense *= 1.15
        print("Coraje de la Legión: +15% defensa")
        self.charge_ultimate(6)
        invoke(lambda: [setattr(ally, 'defense', ally.defense / 1.15) for ally in self.get_allies(radius=6)], delay=5)

    # --- Habilidades básicas y secundarias Vikingos ---
    def wandering_axe(self):
        """Hacha Errante: Daño y sangrado"""
        if self.mana < 22:
            print("No tienes suficiente maná.")
            return
        self.mana -= 22
        target = self.get_enemies(radius=6)[0] if self.get_enemies(radius=6) else None
        if target:
            damage = int(target.max_health * 0.15)
            target.take_damage(damage)
            target.apply_debuff('sangrado', duration=3, tick=lambda e: e.take_damage(int(e.health * 0.03)))
            print("Hacha Errante: Daño y sangrado aplicado")
            self.charge_ultimate(5)

    def wolf_roar(self):
        """Rugido del Lobo: Buff de velocidad de ataque"""
        if self.mana < 18:
            print("No tienes suficiente maná.")
            return
        self.mana -= 18
        for ally in self.get_allies(radius=6):
            if hasattr(ally, 'attack_speed'):
                ally.attack_speed *= 1.12
        print("Rugido del Lobo: +12% velocidad de ataque")
        self.charge_ultimate(4)
        invoke(lambda: [setattr(ally, 'attack_speed', ally.attack_speed / 1.12) for ally in self.get_allies(radius=6) if hasattr(ally, 'attack_speed')], delay=5)

    def shield_charge(self):
        """Embestida de Escudo: Aturde y empuja"""
        if self.mana < 20:
            print("No tienes suficiente maná.")
            return
        self.mana -= 20
        target = self.get_enemies(radius=4)[0] if self.get_enemies(radius=4) else None
        if target:
            target.apply_debuff('aturdimiento', duration=1)
            # Empujar ligeramente (simulación)
            target.position += Vec3(1,0,0)
            print("Embestida de Escudo: Aturdimiento y empuje aplicado")
            self.charge_ultimate(6)

    # --- Habilidades básicas y secundarias Griegos ---
    def shining_arrow(self):
        """Flecha Reluciente: Daño puro"""
        if self.mana < 20:
            print("No tienes suficiente maná.")
            return
        self.mana -= 20
        target = self.get_enemies(radius=6)[0] if self.get_enemies(radius=6) else None
        if target:
            damage = int(target.max_health * 0.18)
            target.take_damage(damage)
            print(f"Flecha Reluciente: {damage} daño puro")
            self.charge_ultimate(5)

    def apollo_touch(self):
        """Toque de Apolo: Curación"""
        if self.mana < 18:
            print("No tienes suficiente maná.")
            return
        self.mana -= 18
        ally = self.get_allies(radius=6)[0] if self.get_allies(radius=6) else None
        if ally:
            ally.health = min(ally.max_health, ally.health + int(ally.max_health * 0.10))
            print("Toque de Apolo: Curación aplicada")
            self.charge_ultimate(4)

    def ares_fury(self):
        """Furia de Ares: Buff de daño de ataque"""
        if self.mana < 24:
            print("No tienes suficiente maná.")
            return
        self.mana -= 24
        self.attack_damage *= 1.15
        print("Furia de Ares: +15% daño de ataque")
        self.charge_ultimate(6)
        invoke(lambda: setattr(self, 'attack_damage', self.attack_damage / 1.15), delay=5)
            
    def ultimate_ability(self):
        """Habilidad definitiva"""
        if self.faction.name == 'Cruzados':
            self.holy_crusade()
        elif self.faction.name == 'Sarracenos':
            self.desert_storm()
        elif self.faction.name == 'Antiguos':
            self.time_manipulation()
        elif self.faction.name == 'Egipcios':
            self.judgement_of_anubis()
        elif self.faction.name == 'Romanos':
            self.neptune_tsunami()
        elif self.faction.name == 'Vikingos':
            self.ragnarok()
        elif self.faction.name == 'Griegos':
            self.olympus_judgement()
    # --- Ultimate de Egipcios ---
    def judgement_of_anubis(self):
        print("¡Juicio de Anubis activado!")
        for enemy in self.get_enemies(radius=7):
            enemy.apply_debuff('veneno', duration=6, tick=lambda e: e.take_damage(int(e.health * 0.07)))
            enemy.take_damage(int(self.magic_power * 1.1))
        for ally in self.get_allies(radius=7):
            ally.health = min(ally.max_health, ally.health + int(ally.max_health * 0.18))
        self.ultimate_charge = 0
        # Efecto visual y sonido aquí

    # --- Ultimate de Romanos ---
    def neptune_tsunami(self):
        print("¡Maremoto de Neptuno activado!")
        for enemy in self.get_enemies(radius=8):
            enemy.apply_debuff('aturdimiento', duration=2)
            enemy.take_damage(int(self.attack_damage * 1.3))
        for ally in self.get_allies(radius=8):
            ally.defense += int(ally.defense * 0.2)
        self.ultimate_charge = 0
        # Efecto visual y sonido aquí

    # --- Ultimate de Vikingos ---
    def ragnarok(self):
        print("¡Ragnarok activado!")
        for enemy in self.get_enemies(radius=9):
            enemy.apply_debuff('congelado', duration=2)
            enemy.take_damage(int(self.attack_damage * 1.5))
        self.berserker_mode(duration=6)
        self.ultimate_charge = 0
        # Efecto visual y sonido aquí

    def berserker_mode(self, duration=6):
        print("Modo Berserker: Daño aumentado, defensa reducida")
        self.attack_damage *= 1.7
        self.defense *= 0.7
        invoke(lambda: self.reset_berserker(), delay=duration)

    def reset_berserker(self):
        self.attack_damage /= 1.7
        self.defense /= 0.7
        print("Modo Berserker finalizado")

    # --- Ultimate de Griegos ---
    def olympus_judgement(self):
        print("¡Juicio del Olimpo activado!")
        for enemy in self.get_enemies(radius=7):
            enemy.take_damage(int(self.magic_power * 1.3))
        for ally in self.get_allies(radius=7):
            ally.health = min(ally.max_health, ally.health + int(ally.max_health * 0.22))
            ally.defense += int(ally.defense * 0.18)
        self.ultimate_charge = 0
        # Efecto visual y sonido aquí
            
    # --- Habilidades básicas y ultimate con efectos reales ---
    # --- Cruzados ---
    def blessing_radiant(self, target):
        """Bendición Radiante: Cura y buff defensa"""
        if self.mana < 30:
            print("No tienes suficiente maná.")
            return
        self.mana -= 30
        heal = int(target.max_health * 0.12)
        target.health = min(target.max_health, target.health + heal)
        target.defense += int(target.defense * 0.1)
        print(f"Bendición Radiante: Curaste {heal} HP y +10% defensa a {target}")
        self.charge_ultimate(8)
        invoke(lambda: setattr(target, 'defense', target.defense // 1.1), delay=4)

    def lance_of_glory(self, enemies):
        """Lanza de Gloria: Daño a hasta 3 enemigos"""
        if self.mana < 40:
            print("No tienes suficiente maná.")
            return
        self.mana -= 40
        for i, enemy in enumerate(enemies[:3]):
            base_damage = self.attack_damage
            extra = base_damage * (0.1 if i > 0 else 0)
            damage = int(base_damage + extra)
            enemy.take_damage(damage)
            print(f"Lanza de Gloria: {damage} daño a {enemy}")
        self.charge_ultimate(10)

    def wall_of_faith(self):
        """Muro de Fe: Escudo circular"""
        if self.mana < 50:
            print("No tienes suficiente maná.")
            return
        self.mana -= 50
        shield = 150 + int(self.defense * 0.2)
        self.shield = shield
        print(f"Muro de Fe: Escudo de {shield} por 5s")
        self.charge_ultimate(12)
        invoke(lambda: setattr(self, 'shield', 0), delay=5)

    # --- Sarracenos ---
    def poisoned_wind(self, enemies):
        """Viento Envenenado: Daño por veneno y ralentización"""
        if self.mana < 35:
            print("No tienes suficiente maná.")
            return
        self.mana -= 35
        for enemy in enemies:
            enemy.apply_debuff('veneno', duration=4, tick=lambda e: e.take_damage(int(e.health * 0.05)))
            enemy.apply_debuff('ralentizacion', duration=2, value=0.8)
        print("Viento Envenenado aplicado")
        self.charge_ultimate(9)

    def sand_seal(self, position, enemies):
        """Sello de Arena: Explosión y aturdimiento"""
        if self.mana < 45:
            print("No tienes suficiente maná.")
            return
        self.mana -= 45
        print(f"Sello de Arena colocado en {position}")
        invoke(lambda: [e.apply_debuff('aturdimiento', duration=1.2) for e in enemies if distance(e.position, position) < 3], delay=2)
        self.charge_ultimate(11)

    def dervish_shield(self):
        """Escudo del Derviche: Bloqueo y reflejo de daño"""
        if self.mana < 25:
            print("No tienes suficiente maná.")
            return
        self.mana -= 25
        self.is_blocking = True
        print("Escudo del Derviche activado")
        self.charge_ultimate(7)
        invoke(lambda: setattr(self, 'is_blocking', False), delay=3)

    # --- Antiguos ---
    def void_whisper(self, enemies):
        """Susurro del Vacío: Daño y corrupción"""
        if self.mana < 40:
            print("No tienes suficiente maná.")
            return
        self.mana -= 40
        for enemy in enemies:
            damage = int(self.magic_power * 1.2)
            enemy.take_damage(damage)
            enemy.apply_debuff('corrupcion', duration=5, tick=lambda e: e.take_damage(int(e.health * 0.03)))
        print("Susurro del Vacío aplicado")
        self.charge_ultimate(10)

    def ethereal_current(self):
        """Corriente Etérea: Teletransporte y espectro"""
        if self.mana < 30:
            print("No tienes suficiente maná.")
            return
        self.mana -= 30
        self.position -= self.forward * 5
        print("Teletransportado 5m atrás")
        # Invoca espectro
        specter = create_test_enemy(position=self.position + Vec3(1,0,1))
        specter.is_specter = True
        specter.attack = lambda target: target.take_damage(int(self.magic_power * 0.05))
        invoke(lambda: specter.disable(), delay=3)
        self.charge_ultimate(8)

    def mark_of_oblivion(self, enemy):
        """Marca del Olvido: Debuff y extiende corrupción"""
        if self.mana < 50:
            print("No tienes suficiente maná.")
            return
        self.mana -= 50
        enemy.apply_debuff('marca_olvido', duration=6, extra_damage=0.15)
        enemy.extend_debuff('corrupcion', extra_duration=2)
        print("Marca del Olvido aplicada")
        self.charge_ultimate(12)

    # --- Ultimate Effects ---
    def holy_crusade(self):
        """Llamado Celestial: Cura masiva y buff aliados"""
        print("¡Llamado Celestial activado!")
        for ally in self.get_allies(radius=8):
            heal = int(ally.max_health * 0.25)
            ally.health = min(ally.max_health, ally.health + heal)
            ally.defense += int(ally.defense * 0.15)
            print(f"Curaste {heal} HP y +15% defensa a {ally}")
        self.ultimate_charge = 0
        # Efecto visual y sonido aquí

    def fury_of_jinn(self):
        """Furia del Jinn: Invoca genio, buff y daño en área"""
        print("¡Furia del Jinn activada!")
        genie = create_test_enemy(position=self.position + Vec3(2,0,2))
        genie.is_genie = True
        for enemy in self.get_enemies(radius=6):
            enemy.take_damage(int(self.attack_damage * 1.2))
            print(f"Furia del Jinn: {enemy} recibe daño")
        self.ultimate_charge = 0
        # Efecto visual y sonido aquí

    def god_of_oblivion(self):
        """Invocación del Dios Olvidado: Debuff masivo y control"""
        print("¡Invocación del Dios Olvidado activada!")
        for enemy in self.get_enemies(radius=7):
            enemy.apply_debuff('dominado', duration=10)
            enemy.take_damage(int(self.magic_power * 1.5))
            print(f"{enemy} dominado y dañado")
        self.ultimate_charge = 0
        # Efecto visual y sonido aquí

    # --- Utilidades ---
    def charge_ultimate(self, percent):
        self.ultimate_charge = min(100, getattr(self, 'ultimate_charge', 0) + percent)
        print(f"Carga de Ultimate: {self.ultimate_charge}%")

    def get_allies(self, radius=8):
        # Devuelve aliados cercanos (placeholder)
        return [self]  # Implementar lógica real

    def get_enemies(self, radius=6):
        # Devuelve enemigos cercanos (placeholder)
        return []
    
    def activate_skill(self, skill_name):
        if skill_name == 'Curación':
            heal_amount = int(self.max_health * 0.25)
            self.health = min(self.health + heal_amount, self.max_health)
            print(f'Curación: +{heal_amount} HP')
            # Efecto visual
            Entity(model='sphere', color=color.lime, position=self.position, scale=0.5)
        elif skill_name == 'Daño en área':
            # Daño a todos los enemigos cercanos
            for e in self.get_nearby_enemies():
                e.health -= 20
                print(f'Daño en área a {e}: -20 HP')
                Entity(model='circle', color=color.red, position=e.position, scale=0.7)
        elif skill_name == 'Invocación':
            # Invoca un aliado temporal
            ally = Entity(model='cube', color=color.azure, position=self.position + (2,0,0), scale=1)
            print('Aliado invocado')
            invoke(destroy, ally, delay=10)
        elif skill_name == 'Ultimate':
            if hasattr(self, 'moral') and self.moral >= 500:
                print(f'Activando ultimate: {self.ultimate}')
                self.moral -= 500
                self.show_ultimate_effect()
            else:
                print('No tienes suficiente fe/moral para activar la ultimate.')

    def get_nearby_enemies(self):
        # Debes conectar esto con el sistema de combate real
        return []

    def show_ultimate_effect(self):
        # Efectos visuales según la ultimate
        if hasattr(self, 'ultimate'):
            if self.ultimate == 'Llama del Mártir':
                Entity(model='quad', color=color.orange, position=self.position + (0,2,0), scale=(2,2,2))
            elif self.ultimate == 'Milagro de Luz':
                Entity(model='sphere', color=color.white, position=self.position, scale=2)
            elif self.ultimate == 'Tornado de Arena':
                Entity(model='circle', color=color.yellow, position=self.position, scale=2)
            elif self.ultimate == 'Fuego Interior':
                Entity(model='sphere', color=color.red, position=self.position, scale=2)
            elif self.ultimate == 'Pisotón del Guardián':
                Entity(model='cube', color=color.brown, position=self.position, scale=2)
            elif self.ultimate == 'Llamado del Bosque':
                Entity(model='circle', color=color.green, position=self.position, scale=2)
            print(f'Efecto visual de {self.ultimate}')
    
    def attack(self):
        self.can_attack = False
        invoke(setattr, self, 'can_attack', True, delay=0.8)
        self.animate_position(self.position + self.forward * 1, duration=0.1, curve=curve.linear)
        self.animate_position(self.position, duration=0.1, delay=0.1, curve=curve.linear)

        enemies_hit = 0
        for ent in scene.entities[:]:
            if isinstance(ent, Enemy) and distance(self, ent) < self.attack_range:
                damage = self.attack_damage + self.stats.get_total_stat('fuerza')
                print(f"Golpeaste al enemigo! Daño: {damage}")
                ent.take_damage(damage)
                enemies_hit += 1
                
        # Actualizar progreso de misiones
        if enemies_hit > 0:
            self.quest_system.update_quest_progress('kill', enemies_hit)
            # Ganar experiencia por matar enemigos
            self.exp_system.add_experience(25 * enemies_hit)

    def take_damage(self, amount):
        self.health -= amount
        if self.health < 0:
            self.health = 0
        print(f"Jugador recibió daño. Vida restante: {self.health}")

    # --- Integración con Guerra de Fe ---
    def calculate_war_power(self):
        base_power = self.auto_combat.calculate_player_power()
        loyalty_bonus = 1 + (self.faction_war_contribution * 0.01)
        return base_power * loyalty_bonus

    def participate_in_guerra_de_fe(self):
        today = datetime.now().date()
        if self.last_contribution_date == today:
            return {'success': False, 'message': 'Ya contribuiste hoy'}
        power = self.calculate_war_power()
        response = faction_war_client.safe_request('POST', 'submit_power', json={
            'player_id': self.id,
            'faction': self.faction.name,
            'power': power
        })
        if response and response.status_code == 200:
            self.last_contribution_date = today
            self.faction_war_contribution += 1
            return {'success': True, 'power_contributed': power}
        return {'success': False, 'message': 'Error al conectar'}
    
    def calcular_dano(self, enemigo):
        base_dano = self.attack_damage
        ventaja = FACTION_ADVANTAGES.get((self.faction.name, enemigo.faction.name), 1.0)
        return base_dano * ventaja

    def mejorar_stat(self, stat):
        costo = get_upgrade_cost(self.level)
        if self.gold >= costo:
            self.stats[stat] += 1
            self.gold -= costo

    # --- Hermandad y Sicarios ---
    def unirse_hermandad(self, hermandad):
        self.hermandad = hermandad
        print(f"Unido a la hermandad: {hermandad}")

    def contratar_sicario(self, sicario, oro):
        if self.gold >= oro:
            self.gold -= oro
            print(f"Sicario {sicario} contratado por {oro} de oro para la guerra de hermandades")
        else:
            print("No tienes suficiente oro para contratar sicario")

    def obtener_arma_legendaria(self, nombre, efecto, server_id):
        self.legendary_item = LegendaryItem(nombre, efecto, server_id)

    def combatir_pvp(self, rival):
        resultado = simulate_pvp(self.stats, rival.stats)
        return resultado

    def enviar_poder_global(self):
        api = APIClient(base_url="https://api.tujuego.com")
        api.send_power_score(self.id, self.faction.name, self.calcular_poder())

    def puede_acceder_premium(self):
        return hasattr(self, 'faith_pass') and self.faith_pass.is_active()

    def reclamar_recompensa_evento(self, evento):
        event_system = EventSystem()
        event_system.claim_event_reward(self, evento)

    def registrar_recompensa_openexus(self, producto):
        api = APIClient(base_url="https://api.opennexus.com")
        api.register_cross_reward(self.id, producto)