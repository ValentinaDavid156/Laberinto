"""Pruebas de la búsqueda determinista del fantasma."""

import pytest


class LaberintoDePrueba:
    def __init__(self, conexiones):
        self.conexiones = conexiones

    def vecinos_accesibles(self, casilla):
        return list(self.conexiones.get(casilla, ()))


def test_camino_valido_en_los_cinco_laberintos(registros):
    from fantasma_ia import buscar_camino
    from laberinto import Laberinto

    for registro in registros:
        laberinto = Laberinto(registro["grid"])
        camino = buscar_camino(laberinto, (0, 0), (14, 14))
        anterior = (0, 0)
        for casilla in camino:
            assert casilla in laberinto.vecinos_accesibles(anterior)
            anterior = casilla
        assert camino[-1] == (14, 14)


def test_camino_origen_igual_a_destino(registros):
    from fantasma_ia import buscar_camino, buscar_camino_con_traza
    from laberinto import Laberinto

    laberinto = Laberinto(registros[0]["grid"])
    origen = (4, 7)
    camino, traza = buscar_camino_con_traza(laberinto, origen, origen)

    assert camino == []
    assert [evento.tipo for evento in traza] == ["apilar", "encontrado"]
    assert traza[-1].casilla == origen
    assert traza[-1].pila == (origen,)
    assert buscar_camino(laberinto, origen, origen) == []


def test_traza_guarda_copias_inmutables_de_la_pila():
    from fantasma_ia import buscar_camino_con_traza

    grafo = LaberintoDePrueba({
        (0, 0): [(1, 0)],
        (1, 0): [(0, 0), (2, 0)],
        (2, 0): [(1, 0)],
    })
    camino, traza = buscar_camino_con_traza(grafo, (0, 0), (2, 0))

    assert camino == [(1, 0), (2, 0)]
    assert all(isinstance(evento.pila, tuple) for evento in traza)
    assert traza[0].pila == ((0, 0),)
    assert traza[-1].pila == ((0, 0), (1, 0), (2, 0))
    with pytest.raises(AttributeError):
        traza[0].pila = ()


def test_traza_hace_retroceso_determinista_y_conserva_su_balance():
    from fantasma_ia import buscar_camino_con_traza

    grafo = LaberintoDePrueba({
        (0, 0): [(1, 0), (0, 1)],
        (1, 0): [(0, 0), (2, 0)],
        (2, 0): [(1, 0)],
        (0, 1): [(0, 0), (1, 1)],
        (1, 1): [(0, 1)],
    })
    camino, traza = buscar_camino_con_traza(grafo, (0, 0), (1, 1))
    _, repetida = buscar_camino_con_traza(grafo, (0, 0), (1, 1))

    assert camino == [(0, 1), (1, 1)]
    assert [evento.tipo for evento in traza] == [
        "apilar", "apilar", "apilar", "desapilar", "desapilar",
        "apilar", "apilar", "encontrado",
    ]
    assert traza[3].casilla == (2, 0)
    assert traza[3].pila == ((0, 0), (1, 0))
    assert traza[4].casilla == (1, 0)
    assert traza[4].pila == ((0, 0),)
    assert traza == repetida
    assert sum(e.tipo == "apilar" for e in traza) - sum(
        e.tipo == "desapilar" for e in traza
    ) == len(camino) + 1


def test_destino_inalcanzable_informa_el_error():
    from fantasma_ia import buscar_camino, buscar_camino_con_traza

    grafo = LaberintoDePrueba({(0, 0): [], (1, 0): []})

    with pytest.raises(ValueError):
        buscar_camino_con_traza(grafo, (0, 0), (1, 0))
    with pytest.raises(ValueError):
        buscar_camino(grafo, (0, 0), (1, 0))
