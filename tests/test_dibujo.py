"""Pruebas de dibujo sobre superficies sin abrir una ventana."""

import pygame

from config import (
    ALTO_VENTANA,
    ANCHO_VENTANA,
    ENTRADA,
    MARGEN,
    META,
    TAM_CELDA,
)
from laberinto import Laberinto


def test_dibujo_pinta_tablero_entrada_y_meta(registros):
    from dibujo import dibujar
    from juego import Partida

    pygame.init()
    superficie = pygame.Surface((ANCHO_VENTANA, ALTO_VENTANA))
    partida = Partida(Laberinto(registros[0]["grid"]))
    dibujar(superficie, partida)

    assert superficie.get_size() == (920, 740)
    assert superficie.get_at((MARGEN + 34, MARGEN + 8))[:3] == ENTRADA
    x_meta = MARGEN + 14 * TAM_CELDA + 10
    y_meta = MARGEN + 14 * TAM_CELDA + 10
    assert superficie.get_at((x_meta, y_meta))[:3] == META


def test_pila_muestra_como_maximo_veinte_bloques():
    from dibujo import bloques_visibles

    pila = tuple((i, 0) for i in range(21))

    visibles, ocultos = bloques_visibles(pila)

    assert len(visibles) == 19
    assert visibles == pila[-19:]
    assert ocultos == 2


def test_pila_de_hasta_veinte_casillas_no_tiene_resumen():
    from dibujo import bloques_visibles

    pila = tuple((i, 0) for i in range(20))

    visibles, ocultos = bloques_visibles(pila)

    assert visibles == pila
    assert ocultos == 0


def test_paredes_tienen_cuatro_pixeles(registros):
    from dibujo import dibujar
    from juego import Partida

    pygame.init()
    laberinto = Laberinto(registros[0]["grid"])
    superficie = pygame.Surface((ANCHO_VENTANA, ALTO_VENTANA))
    dibujar(superficie, Partida(laberinto))

    for fila in range(15):
        for columna in range(15):
            if laberinto.grid[2 * fila + 1][2 * columna + 2] == "#":
                x = MARGEN + columna * TAM_CELDA + 34
                y = MARGEN + fila * TAM_CELDA + 20
                corrida = [
                    superficie.get_at((x + offset, y))[:3] == (0, 0, 0)
                    for offset in range(8)
                ]
                assert max(map(len, "".join("1" if pixel else "0" for pixel in corrida).split("0"))) == 4
                return
    raise AssertionError("El mapa de prueba no contiene paredes internas.")
