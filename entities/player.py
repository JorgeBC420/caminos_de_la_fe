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

faction_war_client = FactionWarClient("https://tujuego.com/api")

class Player(Entity):
    def __init__(self, faction_name='Cruzados', joystick=None, **kwargs):
        super().__init__(**kwargs)
        # --- Datos RPG ---
        self.faction = FACTIONS[faction_name]
        self.model = 'cube'
        self.color = self.faction.color
        self.collider = 'box'
        self.scale = (1, 2, 1)  # Hacer al jugador más alto y visible
        self.speed = GameConfig.PLAYER_SPEED
        self.health = GameConfig.PLAYER_HEALTH
        self.max_health = GameConfig.PLAYER_HEALTH
        self.attack_damage = 15
        self.attack_range = 2.5
        self.can_attack = True

        # --- Sistema de estadísticas ---
        self.stats = PlayerStats(
            base_stats={'fuerza': 12, 'defensa': 8, 'velocidad': 10, 'inteligencia': 5},
            item_bonuses={'fuerza': 2, 'defensa': 1},
            horse_bonuses={'fuerza': 1, 'velocidad': 3}
        )
        self.gold = 100

        # --- Movimiento avanzado ---
        self.velocity = Vec3(0, 0, 0)
        self.gravity = -20
        self.jump_height = 2
        self.on_ground = True
        
        # --- Sistema de experiencia ---
        self.level = self.stats.stats['nivel']
        self.experience = 0
        self.experience_to_next_level = 100 * self.level
        
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

        # --- Joystick Virtual ---
        self.joystick = joystick

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

    # --- Movimiento y combate visual ---
    def update(self):
        # Actualizar el controlador de cámara
        if hasattr(self, 'camera_controller'):
            self.camera_controller.update()
            
        # --- Movimiento con física mejorada ---
        direction = Vec3(0, 0, 0)
        
        # Prioridad 1: Joystick Virtual
        if self.joystick and self.joystick.value.length() > 0:
            direction = Vec3(self.joystick.value.x, 0, self.joystick.value.y).normalized()
        # Prioridad 2: Teclas WASD
        else:
            direction = Vec3(
                held_keys['d'] - held_keys['a'],
                0,
                held_keys['w'] - held_keys['s']
            ).normalized()
            
        # Aplicar movimiento horizontal
        if direction.length() > 0:
            # Calcular velocidad basada en stats
            current_speed = self.speed + (self.stats.get_total_stat('velocidad') * 0.1)
            self.velocity.x = direction.x * current_speed
            self.velocity.z = direction.z * current_speed
            
            # Rotar hacia la dirección de movimiento
            target_rotation = math.degrees(math.atan2(direction.x, direction.z))
            self.rotation_y = lerp(self.rotation_y, target_rotation, time.dt * 10)
        else:
            # Frenar gradualmente
            self.velocity.x = lerp(self.velocity.x, 0, time.dt * 8)
            self.velocity.z = lerp(self.velocity.z, 0, time.dt * 8)
            
        # Aplicar gravedad
        if not self.on_ground:
            self.velocity.y += self.gravity * time.dt
        else:
            self.velocity.y = max(0, self.velocity.y)
            
        # Salto
        if held_keys['space'] and self.on_ground:
            self.velocity.y = self.jump_height * 5
            self.on_ground = False
            
        # Aplicar movimiento
        self.position += self.velocity * time.dt
        
        # Verificar si está en el suelo (simplificado)
        if self.position.y <= 1:  # Asumiendo que el suelo está en y=0 y el jugador mide 2 unidades
            self.position.y = 1
            self.on_ground = True
            self.velocity.y = 0
        else:
            self.on_ground = False
            
        # Regeneración de maná
        if self.mana < self.max_mana:
            mana_regen = 1 + (self.stats.get_total_stat('inteligencia') * 0.1)
            self.mana = min(self.max_mana, self.mana + mana_regen * time.dt)

    def input(self, key):
        # Pasar input al controlador de cámara
        if hasattr(self, 'camera_controller'):
            self.camera_controller.input(key)
            
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

    def use_ability(self, ability_name):
        """Usar una habilidad específica"""
        if ability_name in self.abilities and self.abilities[ability_name]['ready']:
            if ability_name == 'basic_attack':
                self.attack()
            elif ability_name == 'ability1':
                self.faction_ability_1()
                self.quest_system.update_quest_progress('ability', 1)
            elif ability_name == 'ability2':
                self.faction_ability_2()
                self.quest_system.update_quest_progress('ability', 1)
            elif ability_name == 'ultimate':
                self.ultimate_ability()
                self.quest_system.update_quest_progress('ability', 1)
                
    def faction_ability_1(self):
        """Habilidad específica de facción 1"""
        if self.faction.name == 'Cruzados':
            self.crusader_shield()
        elif self.faction.name == 'Sarracenos':
            self.archer_volley()
        elif self.faction.name == 'Antiguos':
            self.ancient_knowledge()
            
    def faction_ability_2(self):
        """Habilidad específica de facción 2"""
        if self.faction.name == 'Cruzados':
            self.divine_strike()
        elif self.faction.name == 'Sarracenos':
            self.swift_movement()
        elif self.faction.name == 'Antiguos':
            self.arcane_blast()
            
    def ultimate_ability(self):
        """Habilidad definitiva"""
        if self.faction.name == 'Cruzados':
            self.holy_crusade()
        elif self.faction.name == 'Sarracenos':
            self.desert_storm()
        elif self.faction.name == 'Antiguos':
            self.time_manipulation()
            
    def crusader_shield(self):
        """Escudo divino - aumenta defensa temporalmente"""
        print("¡Escudo Divino activado!")
        # Implementar lógica de buff defensivo
        
    def archer_volley(self):
        """Lluvia de flechas"""
        print("¡Lluvia de flechas!")
        # Implementar ataque de área
        
    def ancient_knowledge(self):
        """Conocimiento ancestral - regenera maná"""
        print("¡Conocimiento Ancestral!")
        self.mana = min(self.max_mana, self.mana + 50)
        
    def divine_strike(self):
        """Golpe divino - ataque poderoso"""
        print("¡Golpe Divino!")
        # Implementar ataque con daño aumentado
        
    def swift_movement(self):
        """Movimiento rápido - aumenta velocidad"""
        print("¡Movimiento Veloz!")
        # Implementar buff de velocidad
        
    def arcane_blast(self):
        """Explosión arcana - daño mágico"""
        print("¡Explosión Arcana!")
        # Implementar ataque mágico
        
    def holy_crusade(self):
        """Cruzada santa - ultimate de Cruzados"""
        print("¡CRUZADA SANTA!")
        # Implementar habilidad definitiva
        
    def desert_storm(self):
        """Tormenta del desierto - ultimate de Sarracenos"""
        print("¡TORMENTA DEL DESIERTO!")
        # Implementar habilidad definitiva
        
    def time_manipulation(self):
        """Manipulación temporal - ultimate de Antiguos"""
        print("¡MANIPULACIÓN TEMPORAL!")
        # Implementar habilidad definitiva
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

    # --- Integración con guerra de facciones ---
    def calculate_war_power(self):
        base_power = self.auto_combat.calculate_player_power()
        loyalty_bonus = 1 + (self.faction_war_contribution * 0.01)
        return base_power * loyalty_bonus

    def participate_in_war(self):
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