# Inicialización del sistema de hermandades

class Hermandad:
    def __init__(self, nombre, general):
        self.nombre = nombre
        self.general = general
        self.guardianes = []  # máx 3
        self.contratados = []
        self.miembros = [general]
        self.tesoreria = 0
        self.limite_miembros = 25
        self.expansion_nivel = 1
        self.en_guerra = False
        self.donaciones = []
        self.historial_guerra = []

    def es_general(self, jugador):
        return jugador == self.general

    def es_guardian(self, jugador):
        return jugador in self.guardianes

    def puede_administrar(self, jugador):
        return self.es_general(jugador) or self.es_guardian(jugador)

    def invitar(self, jugador, por):
        if self.puede_administrar(por):
            # lógica de invitación
            pass

    def aceptar(self, jugador):
        if len(self.miembros) < self.limite_miembros:
            self.miembros.append(jugador)

    def expulsar(self, jugador, por):
        if self.puede_administrar(por) and jugador in self.miembros:
            self.miembros.remove(jugador)
            if jugador in self.guardianes:
                self.guardianes.remove(jugador)
            if jugador in self.contratados:
                self.contratados.remove(jugador)

    def declarar_guerra(self, otra_hermandad, por):
        if self.puede_administrar(por):
            self.en_guerra = True
            # lógica de guerra

    def donar(self, jugador, cantidad):
        self.tesoreria += cantidad
        self.donaciones.append({'jugador': jugador, 'cantidad': cantidad})

    def devolver_donacion(self, jugador, cantidad, por):
        if self.puede_administrar(por):
            self.tesoreria -= cantidad
            # lógica devolución

    def expandir_fortaleza(self, por):
        if self.puede_administrar(por):
            self.expansion_nivel += 1

    def ampliar_limite(self, cantidad, por):
        if self.puede_administrar(por):
            self.limite_miembros += cantidad

    def contratar(self, jugador, por):
        if self.puede_administrar(por):
            self.contratados.append(jugador)

    def robar_tesoreria(self, otra_hermandad, por):
        if self.en_guerra and self.puede_administrar(por):
            robo = int(otra_hermandad.tesoreria * 0.5)
            otra_hermandad.tesoreria -= robo
            self.tesoreria += robo

    def registrar_guerra(self, resultado):
        self.historial_guerra.append(resultado)
