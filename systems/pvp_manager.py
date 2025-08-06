class PvPManager:
    # Protección (escudo) y cooldowns de ataque
    def set_shield(self, player):
        """Otorga escudo de protección por 30 minutos tras atacar o defender."""
        from datetime import datetime, timedelta
        player.shield_until = datetime.now() + timedelta(minutes=30)
        print(f"{getattr(player, 'name', 'Jugador')} tiene escudo de protección hasta {player.shield_until}")

    def can_attack(self, player):
        """Verifica si el jugador puede atacar según cooldown y tipo de cuenta."""
        from datetime import datetime, timedelta
        last_attack = getattr(player, 'last_attack', None)
        is_premium = getattr(player, 'is_premium', False)
        cooldown = timedelta(minutes=5) if is_premium else timedelta(minutes=10)
        if last_attack and datetime.now() < last_attack + cooldown:
            print(f"Debes esperar antes de atacar de nuevo. Cooldown restante: {(last_attack + cooldown - datetime.now()).seconds//60} min")
            return False
        return True

    def register_attack(self, player):
        """Registra el ataque y actualiza el cooldown."""
        from datetime import datetime
        player.last_attack = datetime.now()
        print(f"{getattr(player, 'name', 'Jugador')} ha atacado. Cooldown iniciado.")

    def is_shielded(self, player):
        """Verifica si el jugador tiene escudo activo."""
        from datetime import datetime
        shield_until = getattr(player, 'shield_until', None)
        if shield_until and datetime.now() < shield_until:
            print(f"{getattr(player, 'name', 'Jugador')} está protegido por escudo.")
            return True
        return False

    # Duelos 1vs1 con apuesta de ítem
    def start_duel(self, opponent, wager_item=None):
        """Inicia un duelo 1vs1 con apuesta de ítem activada."""
        self.duel_opponent = opponent
        self.duel_wager_item = wager_item
        print(f"Duelo iniciado contra {getattr(opponent, 'name', 'oponente')} por el ítem: {wager_item}")

    def resolve_duel(self, winner, loser):
        """Resuelve el duelo, aplica maldición y transfiere el ítem apostado."""
        from datetime import datetime, timedelta
        loser.curse_until = datetime.now() + timedelta(hours=2)
        if not hasattr(loser, 'stat_modifier'):
            loser.stat_modifier = 1.0
        loser.stat_modifier *= 0.85
        print(f"{getattr(loser, 'name', 'Perdedor')} sufre la Maldición del Perdedor (-15% stats por 2h)")
        if self.duel_wager_item:
            if not hasattr(winner, 'unique_items'):
                winner.unique_items = []
            winner.unique_items.append(self.duel_wager_item)
            winner.purification_required = True
            winner.purification_mission_until = datetime.now() + timedelta(hours=24)
            print(f"{getattr(winner, 'name', 'Ganador')} obtiene el ítem único '{self.duel_wager_item}' pero debe purificarlo (misión de 24h)")

    def can_use_unique_item(self, player):
        from datetime import datetime
        if getattr(player, 'purification_required', False):
            if datetime.now() < getattr(player, 'purification_mission_until', datetime.now()):
                print("No puedes usar el ítem único hasta completar la misión de purificación.")
                return False
            else:
                player.purification_required = False
        return True

    def apply_unique_item_risk(self, player):
        from datetime import datetime, timedelta
        if not hasattr(player, 'last_weekly_mission'):
            player.last_weekly_mission = datetime.now() - timedelta(days=8)
        if (datetime.now() - player.last_weekly_mission).days >= 7:
            player.stat_modifier *= 0.9
            player.has_cursed_aura = True
            print("El ítem único maldice al portador (-10% stats, aura visible)")
        else:
            player.has_cursed_aura = False

    def show_unique_item_aura(self, player):
        if getattr(player, 'has_cursed_aura', False):
            print(f"{getattr(player, 'name', 'Jugador')} emite un aura visible: ¡riesgo de ser cazado!")

    # Integración con UI de inventario avanzado y sistema de misiones
    def open_advanced_inventory_ui(self):
        print("[UI] Inventario avanzado abierto.")

    def trigger_mission_for_unique_item(self, player, item):
        print(f"[MISIÓN] Misión de purificación iniciada para {item}.")

    # Anuncios y banners
    def show_popup_ad(self):
        print("[AD] Pop-up mostrado (cada 30 minutos)")

    def show_static_banner(self):
        print("[AD] Banner estático mostrado por 1 minuto (cada 5 minutos)")
    def __init__(self, api_client, player):
        self.api = api_client
        self.player = player

    def find_match(self):
        print("Buscando oponente...")
        import random
        result = {
            'victory': random.choice([True, False]),
            'opponent_name': 'OtroJugador',
            'elo_change': 25 if random.choice([True, False]) else -15
        }
        return result
