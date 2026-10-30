"""Reglas de la partida, separadas del reloj y de la interfaz."""

import random

from dado import Dado
from fantasma_ia import buscar_camino_con_traza

META = (14, 14)
DISTANCIA_MIN_FANTASMA = 6


class Partida:
    JUGADOR_TIRAR = "JUGADOR_TIRAR"
    DADO_JUGADOR = "DADO_JUGADOR"
    JUGADOR_MOVER = "JUGADOR_MOVER"
    APARECE_FANTASMA = "APARECE_FANTASMA"
    FANTASMA_TIRAR = "FANTASMA_TIRAR"
    DADO_FANTASMA = "DADO_FANTASMA"
    FANTASMA_BUSCA = "FANTASMA_BUSCA"
    FANTASMA_MOVER = "FANTASMA_MOVER"
    VICTORIA = "VICTORIA"
    DERROTA = "DERROTA"

    def __init__(self, laberinto, rnd: random.Random | None = None):
        self.laberinto = laberinto
        self.rnd = rnd if rnd is not None else random.Random()
        self.reiniciar()

    def reiniciar(self) -> None:
        self.jugador = (0, 0)
        self.fantasma = None
        self.direccion_fantasma = (0, 1)
        self.turno = 1
        self.estado = self.JUGADOR_TIRAR
        self.pasos_restantes = 0
        self.dado_jugador = Dado(self.rnd)
        self.dado_fantasma = Dado(self.rnd)
        self.camino_fantasma = []
        self.traza_fantasma = []
        self.pasos_fantasma = 0
        self._indice_fantasma = 0

    def tirar_dado_jugador(self) -> int | None:
        if self.estado != self.JUGADOR_TIRAR:
            return None
        self.camino_fantasma = []
        self.traza_fantasma = []
        self.pasos_fantasma = 0
        self.pasos_restantes = 0
        valor = self.dado_jugador.tirar()
        self.estado = self.DADO_JUGADOR
        return valor

    def tirar_dado_fantasma(self) -> int | None:
        if self.estado != self.FANTASMA_TIRAR:
            return None
        valor = self.dado_fantasma.tirar()
        self.estado = self.DADO_FANTASMA
        return valor

    def completar_dado(self) -> bool:
        if self.estado == self.DADO_JUGADOR:
            if self.dado_jugador.animando:
                return False
            self.pasos_restantes = self.dado_jugador.valor
            self.estado = self.JUGADOR_MOVER
            return True

        if self.estado == self.DADO_FANTASMA:
            if self.dado_fantasma.animando:
                return False
            self.camino_fantasma, self.traza_fantasma = buscar_camino_con_traza(
                self.laberinto, self.fantasma, self.jugador
            )
            self.pasos_fantasma = min(
                self.dado_fantasma.valor, len(self.camino_fantasma)
            )
            self._indice_fantasma = 0
            self.estado = self.FANTASMA_BUSCA
            return True
        return False

    def mover_jugador(self, direccion: tuple[int, int]) -> bool:
        if self.estado != self.JUGADOR_MOVER or self.pasos_restantes <= 0:
            return False

        destino = (self.jugador[0] + direccion[0], self.jugador[1] + direccion[1])
        if destino not in self.laberinto.vecinos_accesibles(self.jugador):
            return False

        self.jugador = destino
        self.pasos_restantes -= 1
        if destino == META:
            self.estado = self.VICTORIA
        elif destino == self.fantasma:
            self.estado = self.DERROTA
        elif self.pasos_restantes == 0:
            self.terminar_turno()
        return True

    def terminar_turno(self) -> bool:
        if self.estado != self.JUGADOR_MOVER:
            return False

        self.pasos_restantes = 0
        if self.turno == 1 and self.fantasma is None:
            distancias = self.laberinto.distancias_desde(self.jugador)
            candidatos = [
                casilla for casilla, distancia in distancias.items()
                if distancia >= DISTANCIA_MIN_FANTASMA and casilla != META
            ]
            self.fantasma = self.rnd.choice(candidatos)
            self.estado = self.APARECE_FANTASMA
        else:
            self.estado = self.FANTASMA_TIRAR
        return True

    def completar_aparicion(self) -> bool:
        if self.estado != self.APARECE_FANTASMA:
            return False
        self.estado = self.FANTASMA_TIRAR
        return True

    def completar_busqueda(self) -> bool:
        if self.estado != self.FANTASMA_BUSCA:
            return False
        if self.pasos_fantasma == 0:
            self._terminar_turno_fantasma()
        else:
            self.estado = self.FANTASMA_MOVER
        return True

    def avanzar_fantasma(self) -> bool:
        if (self.estado != self.FANTASMA_MOVER
                or self._indice_fantasma >= self.pasos_fantasma):
            return False

        anterior = self.fantasma
        self.fantasma = self.camino_fantasma[self._indice_fantasma]
        self.direccion_fantasma = (
            self.fantasma[0] - anterior[0], self.fantasma[1] - anterior[1]
        )
        self._indice_fantasma += 1

        if self.fantasma == self.jugador:
            self.estado = self.DERROTA
        elif self._indice_fantasma == self.pasos_fantasma:
            self._terminar_turno_fantasma()
        return True

    def _terminar_turno_fantasma(self) -> None:
        self.turno += 1
        self.estado = self.JUGADOR_TIRAR
