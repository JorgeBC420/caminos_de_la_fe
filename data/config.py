# --- Configuración para AutoCombat (Multiplayer) ---
class AutoCombatConfig:
    BASE_DAMAGE_FORMULA = "enemy_power / (player_defense * 0.5)"
    MINIMUM_DAMAGE_PERCENT = 0.1
    MATCHMAKING_RANGE = 100  # Rango de poder para emparejamiento
    MAX_PLAYERS_PER_BATTLE = 10

# --- Configuración para el modo RPG (Single Player) ---
class GameConfig:
    PLAYER_SPEED = 5
    ENEMY_SPEED = 3
    PLAYER_HEALTH = 100
    ENEMY_HEALTH = 50
    ATTACK_COOLDOWN = 0.8
    CAMERA_DISTANCE = 12
    CAMERA_HEIGHT = 10
    CAMERA_ANGLE = 30
    XP_PER_ENEMY = 20
    PLAYER_DAMAGE = 15
    ENEMY_DAMAGE = 10
    LOOT_DROP_CHANCE = 0.25
    LEVEL_UP_XP = 100
    INVENTORY_SIZE = 30
    MAP_CENTER_COORDS = (0, 0)
    GAME_STATES = ['menu', 'combat', 'paused', 'inventory', 'map']

    # Dificultad dinámica
    @staticmethod
    def get_enemy_difficulty(player_level, player_stats):
        """
        Calcula la dificultad del enemigo según el nivel y los stats del jugador.
        Puedes personalizar la fórmula según tu diseño.
        """
        base = GameConfig.ENEMY_HEALTH + (player_level * 10)
        # Ejemplo: los stats pueden ser un dict con 'strength', 'defense', 'agility'
        difficulty = base + player_stats.get('strength', 0) * 2 - player_stats.get('defense', 0)
        return max(10, difficulty)  # Nunca menos de 10 de vida

    @staticmethod
    def get_enemy_speed(player_level, player_stats):
        """
        Ajusta la velocidad del enemigo según el nivel y agilidad del jugador.
        """
        base_speed = GameConfig.ENEMY_SPEED + (player_level * 0.2)
        agility_bonus = player_stats.get('agility', 0) * 0.05
        return base_speed + agility_bonus