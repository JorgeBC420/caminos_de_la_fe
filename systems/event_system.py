import time

class EventSystem:
    events = {
        'holy_war': {'active': False, 'participants': []},
        'item_purification': {'player': None, 'timer': 0}
    }
    
    def start_event(self, event_name, data):
        self.events[event_name] = {**data, 'start_time': time.time()}

    def end_event(self, event_name, player, ui=None):
        """
        Finaliza el evento y convierte monedas de evento en oro usando EconomyManager.
        Muestra mensaje en la UI si se provee.
        """
        from systems.economy_manager import EconomyManager
        oro_ganado = EconomyManager.convert_event_currency_to_gold(player)
        msg = f"Evento '{event_name}' finalizado. Has convertido tus monedas de evento en {oro_ganado} oro."
        print(msg)
        if ui:
            try:
                ui.message = msg
            except Exception:
                from ursina import Text, color
                Text(text=msg, y=0.4, color=color.green)
