# Módulo de combate PvP

class PvPSystem:
    def __init__(self):
        self.protecciones = {}

    def puede_atacar(self, atacante, defensor):
        # Niveles y protección
        if self.verificar_proteccion(defensor):
            return False
        if atacante.nivel < 10:
            return abs(atacante.nivel - defensor.nivel) <= 5
        return True

    def atacar(self, atacante, defensor):
        if not self.puede_atacar(atacante, defensor):
            return 'Defensor protegido'
        # Simulación de combate
        while atacante.ps > defensor.ps * 0.25 and defensor.ps > atacante.ps * 0.25:
            atacante.ps -= atacante.dps
            defensor.ps -= defensor.dps
        if atacante.ps <= atacante.ps_max * 0.25:
            self.otorgar_proteccion(atacante)
        if defensor.ps <= defensor.ps_max * 0.25:
            self.otorgar_proteccion(defensor)
        return 'Combate simulado'

    def otorgar_proteccion(self, jugador, minutos=30):
        self.protecciones[jugador] = minutos

    def verificar_proteccion(self, jugador):
        return self.protecciones.get(jugador, 0) > 0

    def debilitar(self, jugador, porcentaje=0.25):
        jugador.ps = max(jugador.ps * porcentaje, 1)
