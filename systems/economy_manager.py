from data.config import EconomyConfig

class EconomyManager:
    @staticmethod
    def convert_event_currency_to_gold(player, ratio=1.01):
        """
        Convierte todas las monedas de evento del jugador en oro al finalizar el evento.
        El ratio por defecto es 1 moneda de evento = 1.01 oro.
        """
        if hasattr(player, 'event_currency') and player.event_currency > 0:
            oro_ganado = int(player.event_currency * ratio)
            player.gold += oro_ganado
            print(f"Has convertido {player.event_currency} monedas de evento en {oro_ganado} oro.")
            player.event_currency = 0
            return oro_ganado
        print("No tienes monedas de evento para convertir.")
        return 0
    @staticmethod
    def get_gold_value(usd_price, player_level):
        """Calcula el VALOR en ORO de un objeto premium para mostrarlo en la UI, con equivalencia exacta."""
        if player_level <= 10:
            oro_por_usd = 1000
        else:
            oro_por_usd = 100 * player_level
        return int(usd_price * oro_por_usd)

    @staticmethod
    def can_afford(player, item_key):
        """Verifica si el jugador puede comprar un objeto con las monedas permitidas y oro."""
        item_costs = EconomyConfig.PREMIUM_ITEMS[item_key]
        gold_value = EconomyManager.get_gold_value(item_costs['usd'], player.level)
        afford_gold = player.gold >= gold_value
        afford_event = player.event_currency >= item_costs['event']
        return {'gold': afford_gold, 'event': afford_event}

    @staticmethod
    def purchase_item(player, item_key, currency_type):
        """Procesa la compra. Permite oro, evento y USD. Aplica quema y devaluación si corresponde."""
        item_costs = EconomyConfig.PREMIUM_ITEMS[item_key]
        gold_value = EconomyManager.get_gold_value(item_costs['usd'], player.level)
        if currency_type == 'gold':
            if player.gold >= gold_value:
                # Quema el 30% del oro usado
                burn_amount = int(gold_value * 0.3)
                player.gold -= gold_value
                # Devaluación: reduce oro restante un 0.5%
                player.gold = int(player.gold * 0.995)
                # Opcional: registrar oro quemado si se requiere
                return True
        elif currency_type == 'event':
            if player.event_currency >= item_costs['event']:
                player.event_currency -= item_costs['event']
                return True
        elif currency_type == 'usd':
            # ... Iniciar proceso de compra con dinero real ...
            return True # Suponiendo que la compra es exitosa
        return False

    @staticmethod
    def get_daily_gold_limit(player, source='mission'):
        """
        Devuelve el límite diario de oro que puede farmear el jugador según su nivel.
        Solo aplica a misiones (source='mission'). PvP no tiene límite.
        """
        if source == 'pvp':
            return None  # Sin límite para PvP
        if player.level <= 30:
            return 5000
        elif player.level <= 60:
            return 7000
        else:
            return 10000
