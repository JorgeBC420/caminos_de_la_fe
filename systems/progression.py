# Sistema de progresión (niveles, experiencia)
from ursina import *

class ExperienceSystem:
    def __init__(self, player):
        self.player = player
        self.experience_curve = 1.2  # Factor exponencial
        self.base_experience = 100   # EXP base para nivel 2
        
    def calculate_experience_for_level(self, level):
        """Calcula la experiencia total necesaria para alcanzar un nivel"""
        if level <= 1:
            return 0
        return int(self.base_experience * (level - 1) ** self.experience_curve)
    
    def calculate_experience_to_next_level(self, current_level):
        """Calcula cuánta experiencia falta para el siguiente nivel"""
        current_total = self.calculate_experience_for_level(current_level)
        next_total = self.calculate_experience_for_level(current_level + 1)
        return next_total - current_total
    
    def add_experience(self, amount):
        """Añade experiencia y maneja el subir de nivel"""
        self.player.experience += amount
        print(f"+{amount} EXP")
        
        # Verificar si puede subir de nivel
        while self.can_level_up():
            self.level_up()
    
    def can_level_up(self):
        """Verifica si el jugador puede subir de nivel"""
        required_exp = self.calculate_experience_for_level(self.player.level + 1)
        return self.player.experience >= required_exp
    
    def level_up(self):
        """Sube al jugador de nivel"""
        old_level = self.player.level
        self.player.level += 1
        self.player.stats.stats['nivel'] = self.player.level
        
        # Recompensas por subir de nivel
        self.player.gold += 50 * self.player.level  # Oro escalado
        stat_points = 3  # Puntos de estadística por nivel
        
        # Aumentar stats automáticamente (balanceado por facción)
        if self.player.faction.name == 'Cruzados':
            self.player.stats.stats['fuerza'] += 1
            self.player.stats.stats['defensa'] += 1
            self.player.stats.stats['resistencia'] += 1
        elif self.player.faction.name == 'Sarracenos':
            self.player.stats.stats['destreza'] += 1
            self.player.stats.stats['velocidad'] += 1
            self.player.stats.stats['agilidad'] += 1
        elif self.player.faction.name == 'Antiguos':
            self.player.stats.stats['inteligencia'] += 2
            self.player.stats.stats['tecnica'] += 1
        
        # Recalcular vida y maná máximos
        self.player.stats.max_health = self.player.stats.calculate_max_health()
        self.player.stats.max_mana = self.player.stats.calculate_max_mana()
        
        # Restaurar vida y maná al subir de nivel
        self.player.health = self.player.stats.max_health
        self.player.mana = self.player.stats.max_mana
        
        print(f"¡NIVEL {self.player.level}!")
        print(f"¡+{50 * self.player.level} oro!")
        print("¡Vida y maná restaurados!")
        
        # Actualizar UI si existe
        if hasattr(self.player, 'stats_ui') and self.player.stats_ui:
            self.player.stats_ui.update_ui()

    def get_upgrade_cost(level):
        return (level + 1) ** 2

class QuestSystem:
    def __init__(self, player):
        self.player = player
        self.active_quests = []
        self.completed_quests = []
        self.available_quests = self.generate_daily_quests()
        
    def generate_daily_quests(self):
        """Genera misiones diarias aleatorias"""
        base_quests = [
            {
                'id': 'kill_enemies',
                'name': 'Eliminar Enemigos',
                'description': 'Derrota a 5 enemigos',
                'type': 'kill',
                'target': 5,
                'progress': 0,
                'rewards': {'gold': 100, 'experience': 150}
            },
            {
                'id': 'collect_gold',
                'name': 'Recolectar Oro',
                'description': 'Recolecta 200 monedas de oro',
                'type': 'collect',
                'target': 200,
                'progress': 0,
                'rewards': {'gold': 300, 'experience': 100}
            },
            {
                'id': 'use_abilities',
                'name': 'Usar Habilidades',
                'description': 'Usa habilidades de facción 10 veces',
                'type': 'ability',
                'target': 10,
                'progress': 0,
                'rewards': {'gold': 150, 'experience': 200}
            }
        ]
        return base_quests[:2]  # Solo 2 misiones diarias inicialmente
        
    def accept_quest(self, quest_id):
        """Acepta una misión disponible"""
        for quest in self.available_quests:
            if quest['id'] == quest_id:
                self.active_quests.append(quest)
                self.available_quests.remove(quest)
                print(f"Misión aceptada: {quest['name']}")
                return True
        return False
        
    def update_quest_progress(self, quest_type, amount=1):
        """Actualiza el progreso de las misiones activas"""
        for quest in self.active_quests:
            if quest['type'] == quest_type:
                quest['progress'] += amount
                print(f"Progreso de misión: {quest['name']} ({quest['progress']}/{quest['target']})")
                
                if quest['progress'] >= quest['target']:
                    self.complete_quest(quest)
                    
    def complete_quest(self, quest):
        """Completa una misión y otorga recompensas"""
        self.active_quests.remove(quest)
        self.completed_quests.append(quest)
        
        # Otorgar recompensas
        rewards = quest['rewards']
        if 'gold' in rewards:
            self.player.gold += rewards['gold']
            print(f"+{rewards['gold']} oro")
            
        if 'experience' in rewards:
            if hasattr(self.player, 'exp_system'):
                self.player.exp_system.add_experience(rewards['experience'])
                
        print(f"¡Misión completada: {quest['name']}!")

class DailyRewardSystem:
    def __init__(self, player):
        self.player = player
        self.current_streak = 1
        self.last_claim_date = None
        
        self.rewards = {
            1: {'gold': 100, 'experience': 50},
            2: {'gold': 150, 'experience': 75},
            3: {'gold': 200, 'experience': 100},
            4: {'gold': 250, 'experience': 125},
            5: {'gold': 300, 'experience': 150},
            6: {'gold': 400, 'experience': 200},
            7: {'gold': 500, 'experience': 300, 'special': 'faction_token'}  # Día 7 especial
        }
        
    def can_claim_daily_reward(self):
        """Verifica si se puede reclamar la recompensa diaria"""
        from datetime import datetime, timedelta
        today = datetime.now().date()
        
        if self.last_claim_date is None:
            return True
            
        if self.last_claim_date < today:
            return True
            
        return False
        
    def claim_daily_reward(self):
        """Reclama la recompensa diaria"""
        if not self.can_claim_daily_reward():
            print("Ya reclamaste tu recompensa diaria hoy")
            return False
            
        from datetime import datetime, timedelta
        today = datetime.now().date()
        
        # Verificar si mantuvo la racha
        if self.last_claim_date and (today - self.last_claim_date).days > 1:
            self.current_streak = 1  # Reiniciar racha
        elif self.last_claim_date and (today - self.last_claim_date).days == 1:
            self.current_streak = min(7, self.current_streak + 1)  # Continuar racha (máximo 7)
            
        self.last_claim_date = today
        
        # Otorgar recompensas
        day_reward = self.rewards.get(self.current_streak, self.rewards[7])
        
        if 'gold' in day_reward:
            self.player.gold += day_reward['gold']
            print(f"Recompensa diaria día {self.current_streak}: +{day_reward['gold']} oro")
            
        if 'experience' in day_reward:
            if hasattr(self.player, 'exp_system'):
                self.player.exp_system.add_experience(day_reward['experience'])
                
        if 'special' in day_reward:
            print(f"¡Recompensa especial: {day_reward['special']}!")
            
        return True
