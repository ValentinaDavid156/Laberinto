"""Interfaz principal y bucle de ejecución del juego."""

import argparse
import os
from pathlib import Path
import random

os.environ.setdefault("PYGAME_HIDE_SUPPORT_PROMPT", "1")
import pygame

import config
from dibujo import dibujar, dibujar_final, dibujar_menu
from juego import Partida
from laberinto import cargar_catalogo
from visualizador import ReproductorTraza


MAPA_FIJO = 4


class Aplicacion:
    MENU = "MENU"
    JUEGO = "JUEGO"

    def __init__(self, semilla=None):
        self.semilla = semilla
        self.rnd = random.Random(semilla)
        self.pantalla = self.MENU
        self.visualizador_activado = True
        self.saliendo = False
        self.partida = None
        self.reproductor = ReproductorTraza()
        self.mapa_id = MAPA_FIJO
        self._tiempo_estado = 0.0
        self._tiempo_paso_fantasma = 0.0
        self._tiempo_evento = 0.0
        ruta = Path(__file__).resolve().parent / "base" / "laberintos.json"
        catalogo = cargar_catalogo(ruta)
        entrada = next(
            (item for item in catalogo.entradas if item.datos.get("id") == MAPA_FIJO),
            None,
        )
        if entrada is None:
            raise RuntimeError("No se encontró el laberinto fijo número 4.")
        self.laberinto = entrada.laberinto

    def manejar_tecla(self, tecla):
        if self.pantalla == self.MENU:
            if tecla == pygame.K_ESCAPE:
                self.saliendo = True
            elif tecla == pygame.K_v:
                self.visualizador_activado = not self.visualizador_activado
            elif tecla in (pygame.K_RETURN, pygame.K_KP_ENTER):
                self._iniciar_partida()
            return

        if self.partida is None:
            return
        estado = self.partida.estado
        if estado in (self.partida.VICTORIA, self.partida.DERROTA):
            if tecla == pygame.K_r:
                self.partida.reiniciar()
                self.reproductor.limpiar()
                self._tiempo_estado = 0.0
                self._tiempo_paso_fantasma = 0.0
                self._tiempo_evento = 0.0
            elif tecla in (pygame.K_m, pygame.K_ESCAPE):
                self._volver_al_menu()
            return

        if tecla == pygame.K_ESCAPE:
            self._volver_al_menu()
        elif estado == self.partida.JUGADOR_TIRAR and tecla == pygame.K_SPACE:
            self.reproductor.limpiar()
            self.partida.tirar_dado_jugador()
        elif estado == self.partida.JUGADOR_MOVER:
            direcciones = {
                pygame.K_UP: (0, -1),
                pygame.K_RIGHT: (1, 0),
                pygame.K_DOWN: (0, 1),
                pygame.K_LEFT: (-1, 0),
            }
            if tecla in direcciones:
                self.partida.mover_jugador(direcciones[tecla])
            elif tecla in (pygame.K_RETURN, pygame.K_KP_ENTER):
                self.partida.terminar_turno()
        elif estado == self.partida.FANTASMA_BUSCA:
            if tecla == pygame.K_p:
                self.reproductor.pausar()
            elif tecla == pygame.K_n:
                if self.reproductor.avanzar_uno():
                    self._tiempo_evento = 0.0
            elif tecla == pygame.K_s:
                self.reproductor.saltar()
                self.reproductor.pausado = False
                self._tiempo_evento = 0.0
            elif tecla in (pygame.K_PLUS, pygame.K_EQUALS, pygame.K_KP_PLUS):
                self.reproductor.acelerar()
            elif tecla in (pygame.K_MINUS, pygame.K_KP_MINUS):
                self.reproductor.reducir()

    def actualizar(self, dt):
        if self.pantalla != self.JUEGO or self.partida is None:
            return
        self.partida.dado_jugador.actualizar(dt)
        self.partida.dado_fantasma.actualizar(dt)
        estado = self.partida.estado

        if estado == self.partida.DADO_JUGADOR:
            self.partida.completar_dado()
        elif estado == self.partida.APARECE_FANTASMA:
            self._tiempo_estado += max(0.0, dt)
            if self._tiempo_estado >= 1.0:
                self.partida.completar_aparicion()
                self.partida.tirar_dado_fantasma()
                self._tiempo_estado = 0.0
        elif estado == self.partida.DADO_FANTASMA:
            if self.partida.completar_dado():
                self.reproductor.iniciar(self.partida.traza_fantasma)
                self._tiempo_evento = 0.0
        elif estado == self.partida.FANTASMA_BUSCA:
            indice = self.reproductor.indice
            if not self.reproductor.terminado:
                self.reproductor.actualizar(dt)
            if self.reproductor.indice != indice:
                self._tiempo_evento = 0.0
            elif not self.reproductor.pausado:
                self._tiempo_evento += max(0.0, dt)
            espera_final = (
                self.reproductor.activado
                and self.reproductor.evento_actual is not None
                and self.reproductor.evento_actual.tipo == "encontrado"
                and self._tiempo_evento < 0.48
            )
            if self.reproductor.terminado and not espera_final:
                self.partida.completar_busqueda()
                self._tiempo_paso_fantasma = 0.0
        elif estado == self.partida.FANTASMA_MOVER:
            self._tiempo_paso_fantasma += max(0.0, dt)
            while (self._tiempo_paso_fantasma >= 0.25
                   and self.partida.estado == self.partida.FANTASMA_MOVER):
                self._tiempo_paso_fantasma -= 0.25
                self.partida.avanzar_fantasma()

    def dibujar(self, superficie):
        if self.pantalla == self.MENU:
            dibujar_menu(superficie, self.visualizador_activado)
            return
        mensaje = ""
        if self.partida.estado == self.partida.FANTASMA_BUSCA:
            mensaje = (
                "El fantasma busca tu rastro…  "
                "(P pausa · N paso · S saltar · +/- velocidad)"
            )
        dibujar(
            superficie,
            self.partida,
            self.reproductor,
            self.partida.dado_jugador,
            self.partida.dado_fantasma,
            mensaje,
            self._tiempo_evento,
            min(0.12, self.reproductor.intervalo),
        )
        if self.partida.estado in (self.partida.VICTORIA, self.partida.DERROTA):
            dibujar_final(superficie, self.partida)

    def _iniciar_partida(self):
        self.partida = Partida(self.laberinto, self.rnd)
        self.reproductor = ReproductorTraza(self.visualizador_activado)
        self.pantalla = self.JUEGO
        self._tiempo_estado = 0.0
        self._tiempo_paso_fantasma = 0.0
        self._tiempo_evento = 0.0

    def _volver_al_menu(self):
        self.pantalla = self.MENU
        self.partida = None
        self.reproductor.limpiar()
        self._tiempo_estado = 0.0
        self._tiempo_paso_fantasma = 0.0
        self._tiempo_evento = 0.0


def crear_parser():
    parser = argparse.ArgumentParser(description="El Laberinto del Fantasma")
    parser.add_argument(
        "--semilla",
        type=_convertir_semilla,
        help="semilla entera para repetir la partida",
    )
    return parser


def _convertir_semilla(texto):
    try:
        return int(texto)
    except ValueError as error:
        raise argparse.ArgumentTypeError(
            "la semilla debe ser un número entero"
        ) from error


def main(argumentos=None):
    opciones = crear_parser().parse_args(argumentos)
    pygame.init()
    ventana = pygame.display.set_mode((config.ANCHO_VENTANA, config.ALTO_VENTANA))
    pygame.display.set_caption("El Laberinto del Fantasma")
    aplicacion = Aplicacion(opciones.semilla)
    reloj = pygame.time.Clock()
    while not aplicacion.saliendo:
        dt = reloj.tick(config.FPS) / 1000
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                aplicacion.saliendo = True
            elif evento.type == pygame.KEYDOWN:
                aplicacion.manejar_tecla(evento.key)
        aplicacion.actualizar(dt)
        aplicacion.dibujar(ventana)
        pygame.display.flip()
    pygame.quit()


if __name__ == "__main__":
    main()
