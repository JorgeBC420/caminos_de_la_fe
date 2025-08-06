# Interfaz de guerra: aliados, contratados, zona segura
class Guerra:
    def __init__(self):
        self.aliados = []
        self.contratados = []
        self.zona_segura = True
    def agregar_aliado(self, jugador):
        self.aliados.append(jugador)
    def agregar_contratado(self, jugador):
        self.contratados.append(jugador)
    def trasladar_a_campo_batalla(self, jugador):
        # 30 min antes
        pass
    def activar_zona_segura(self):
        self.zona_segura = True
    def desactivar_zona_segura(self):
        self.zona_segura = False
