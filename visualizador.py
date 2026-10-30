"""Reproducción de trazas de búsqueda, sin dependencias gráficas."""


class ReproductorTraza:
    def __init__(self, activado=True):
        self.activado = activado
        self.velocidad = 1.0
        self.limpiar()

    def limpiar(self):
        self.traza = ()
        self.indice = 0
        self.evento_actual = None
        self.pila_visible = ()
        self.en_pila = set()
        self.descartadas = set()
        self.camino_encontrado = ()
        self.apilados = 0
        self.desapilados = 0
        self.profundidad_maxima = 0
        self.acumulado = 0.0
        self.pausado = False
        self.terminado = False
        self.esperando = True

    @property
    def profundidad_actual(self):
        return len(self.pila_visible)

    @property
    def intervalo(self):
        if not self.traza:
            return max(0.03, 4.0) / self.velocidad
        return max(0.03, 4.0 / len(self.traza)) / self.velocidad

    @property
    def cima(self):
        return self.pila_visible[-1] if self.pila_visible else None

    def iniciar(self, traza):
        self.limpiar()
        self.traza = tuple(traza)
        if not self.traza:
            return False
        self.esperando = False
        if not self.activado:
            self.saltar()
        return True

    def actualizar(self, dt):
        if self.esperando or self.terminado or self.pausado:
            return
        self.acumulado += max(0.0, dt)
        while self.acumulado >= self.intervalo and not self.terminado:
            self.acumulado -= self.intervalo
            self._avanzar()

    def pausar(self):
        if not self.esperando and not self.terminado:
            self.pausado = not self.pausado

    def avanzar_uno(self):
        if not self.pausado or self.terminado:
            return False
        self._avanzar()
        return True

    def saltar(self):
        while self.indice < len(self.traza):
            self._avanzar()

    def acelerar(self):
        self.velocidad = min(4.0, self.velocidad * 2)

    def reducir(self):
        self.velocidad = max(0.25, self.velocidad / 2)

    def estado_casilla(self, casilla):
        if casilla in self.camino_encontrado:
            return "camino"
        if casilla in self.en_pila:
            return "en_pila"
        if casilla in self.descartadas:
            return "descartada"
        return None

    def _avanzar(self):
        if self.indice >= len(self.traza):
            self.terminado = True
            return
        evento = self.traza[self.indice]
        self.indice += 1
        self.evento_actual = evento
        if evento.tipo == "apilar":
            self.apilados += 1
            self.en_pila.add(evento.casilla)
        elif evento.tipo == "desapilar":
            self.desapilados += 1
            self.en_pila.discard(evento.casilla)
            self.descartadas.add(evento.casilla)
        elif evento.tipo == "encontrado":
            self.camino_encontrado = evento.pila[1:]
        self.pila_visible = evento.pila
        self.profundidad_maxima = max(self.profundidad_maxima, len(evento.pila))
        if self.indice == len(self.traza):
            self.terminado = True
