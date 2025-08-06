# Economía: mercado general, venta directa, restricciones
class Mercado:
    def __init__(self):
        self.items = []
    def vender(self, vendedor, item, valor):
        vendedor.oro += int(valor * 0.75)
        self.items.append({'item': item, 'valor': valor, 'vendedor': vendedor})
    def comprar(self, comprador, item):
        for i in self.items:
            if i['item'] == item:
                comprador.oro -= i['valor']
                self.items.remove(i)
                break
    def venta_directa(self, vendedor, item, valor):
        vendedor.oro += int(valor * 0.5)
