from ursina import *
from systems.economy_manager import EconomyManager
from data.config import EconomyConfig

class PremiumStoreUI(Entity):
    def __init__(self, player, **kwargs):
        super().__init__(parent=camera.ui, **kwargs)
        self.player = player
        # ... (código para crear el panel de la tienda) ...
        self.show_item('cambio_faccion')

    def show_item(self, item_key):
        # Limpiar la vista anterior
        # ...
        item_costs = EconomyConfig.PREMIUM_ITEMS[item_key]
        gold_value = EconomyManager.get_gold_value(item_costs['usd'], self.player.level)
        Text(text="Cambio de Facción", y=0.3)
        # ANCLAJE DE VALOR: Mostramos el "precio" en oro
        Text(text=f"(Valor: {gold_value} ORO)", y=0.2, color=color.gray)
        # Solo botones de compra con USD y Sellos de Evento
        Button(text=f"Comprar por ${item_costs['usd']:.2f} USD", y=0.05,
               on_click=lambda: self.buy(item_key, 'usd'))
        Button(text=f"Comprar por {item_costs['event']} Sellos", y=-0.1,
               on_click=lambda: self.buy(item_key, 'event'))

    def buy(self, item_key, currency):
        success = EconomyManager.purchase_item(self.player, item_key, currency)
        if success:
            print(f"Compra exitosa de {item_key} usando {currency}")
        else:
            print(f"No se pudo completar la compra de {item_key} usando {currency}")
