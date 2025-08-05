import random

def calcular_resultado_asedio(jugador_stats, unidades_jugador, stats_enemigas):
    poder_jugador = sum(jugador_stats.values()) + sum(unidades_jugador)
    poder_enemigo = sum(stats_enemigas.values())
    random_factor = random.uniform(0.85, 1.15)
    resultado = (poder_jugador * random_factor) > poder_enemigo
    return resultado

def simulate_pvp(player_stats, opponent_stats):
    score = sum(player_stats.values()) - sum(opponent_stats.values())
    return score + random.randint(-5, 5) > 0
