"""Búsqueda determinista del fantasma con una pila explícita."""

from typing import Literal, NamedTuple

Casilla = tuple[int, int]


class Evento(NamedTuple):
    tipo: Literal["apilar", "desapilar", "encontrado"]
    casilla: Casilla
    pila: tuple[Casilla, ...]


def buscar_camino_con_traza(
    laberinto, origen: Casilla, destino: Casilla
) -> tuple[list[Casilla], list[Evento]]:
    """Devolver el camino al destino y los cambios de la pila."""
    pila = [origen]
    visitadas = {origen}
    traza = [Evento("apilar", origen, tuple(pila))]

    while pila:
        actual = pila[-1]
        if actual == destino:
            traza.append(Evento("encontrado", destino, tuple(pila)))
            return pila[1:], traza

        for vecino in laberinto.vecinos_accesibles(actual):
            if vecino not in visitadas:
                visitadas.add(vecino)
                pila.append(vecino)
                traza.append(Evento("apilar", vecino, tuple(pila)))
                break
        else:
            casilla = pila.pop()
            traza.append(Evento("desapilar", casilla, tuple(pila)))

    raise ValueError("No existe un camino entre el origen y el destino.")


def buscar_camino(laberinto, origen: Casilla, destino: Casilla) -> list[Casilla]:
    """Devolver solo las casillas del camino, sin incluir el origen."""
    camino, _ = buscar_camino_con_traza(laberinto, origen, destino)
    return camino
