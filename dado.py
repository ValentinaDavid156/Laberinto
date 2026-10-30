"""Tiradas reproducibles y animación independiente del resultado lógico."""

import random


class Dado:
    DURACION_ANIMACION = 0.6
    INTERVALO_CARA = 0.06

    def __init__(self, rnd_logico: random.Random, rnd_visual=None):
        self.rnd_logico = rnd_logico
        self.rnd_visual = rnd_visual if rnd_visual is not None else random.Random()
        self.valor = None
        self.cara_visible = None
        self.animando = False
        self._tiempo = 0.0
        self._proximo_cambio = self.INTERVALO_CARA

    def tirar(self) -> int:
        """Iniciar una tirada; repetir la orden no cambia una animación activa."""
        if not self.animando:
            self.valor = self.rnd_logico.randint(1, 6)
            self.cara_visible = self.rnd_visual.randint(1, 6)
            self.animando = True
            self._tiempo = 0.0
            self._proximo_cambio = self.INTERVALO_CARA
        return self.valor

    def actualizar(self, dt: float) -> None:
        """Avanzar la animación sin consumir la fuente aleatoria lógica."""
        if not self.animando:
            return

        self._tiempo += max(0.0, dt)
        while (self._proximo_cambio < self.DURACION_ANIMACION
               and self._tiempo >= self._proximo_cambio):
            self.cara_visible = self.rnd_visual.randint(1, 6)
            self._proximo_cambio += self.INTERVALO_CARA

        if self._tiempo >= self.DURACION_ANIMACION:
            self.animando = False
            self.cara_visible = self.valor
