# Módulo del hogar del jugador

class Hogar:
    def __init__(self, propietario):
        self.propietario = propietario
        self.nivel = 1
        self.regeneracion_ps = 0.25  # 25% por tiempo
        self.recoleccion_oro = 0.05  # 5% pasivo
        self.mejoras = []

    def regenerar_ps(self, jugador):
        jugador.ps = min(jugador.ps + jugador.ps_max * self.regeneracion_ps, jugador.ps_max)

    def recolectar_oro(self, jugador):
        jugador.oro += int(jugador.oro * self.recoleccion_oro)

    def mejorar(self):
        self.nivel += 1
        self.regeneracion_ps += 0.05
        self.recoleccion_oro += 0.02
        self.mejoras.append(f"Mejora nivel {self.nivel}")
