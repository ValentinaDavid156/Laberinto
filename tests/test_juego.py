"""Pruebas de turnos, movimientos y persecución del fantasma."""

import random


class AzarControlado(random.Random):
    def __init__(self, tiradas=()):
        super().__init__(31)
        self.tiradas = list(tiradas)

    def randint(self, minimo, maximo):
        valor = self.tiradas.pop(0) if self.tiradas else minimo
        assert minimo <= valor <= maximo
        return valor


def nueva_partida(registros, tiradas=()):
    from juego import Partida
    from laberinto import Laberinto

    azar = AzarControlado(tiradas)
    return Partida(Laberinto(registros[3]["grid"]), azar), azar


def completar_tirada_jugador(partida):
    partida.tirar_dado_jugador()
    assert not partida.completar_dado()
    partida.dado_jugador.actualizar(0.6)
    partida.completar_dado()


def test_inicio_y_ordenes_ignoradas_fuera_de_estado(registros):
    partida, _ = nueva_partida(registros)

    assert partida.estado == "JUGADOR_TIRAR"
    assert partida.turno == 1
    assert partida.jugador == (0, 0)
    assert partida.fantasma is None
    assert not partida.mover_jugador((1, 0))
    partida.terminar_turno()
    assert partida.estado == "JUGADOR_TIRAR"
    assert partida.jugador == (0, 0)


def test_pared_no_gasta_pasos_y_movimiento_valido_si(registros):
    partida, _ = nueva_partida(registros, [2])
    completar_tirada_jugador(partida)
    laberinto = partida.laberinto
    vecinos = laberinto.vecinos_accesibles(partida.jugador)
    destino = vecinos[0]
    direccion = (destino[0], destino[1])

    assert partida.mover_jugador(direccion)
    assert partida.jugador == destino
    assert partida.pasos_restantes == 1

    bloqueada = next(
        (dc, df) for dc, df in ((0, -1), (1, 0), (0, 1), (-1, 0))
        if (partida.jugador[0] + dc, partida.jugador[1] + df)
        not in laberinto.vecinos_accesibles(partida.jugador)
    )
    assert not partida.mover_jugador(bloqueada)
    assert partida.pasos_restantes == 1


def test_sin_pasos_no_se_mueve_y_el_primer_turno_aparece_el_fantasma(registros):
    partida, _ = nueva_partida(registros, [1])
    completar_tirada_jugador(partida)
    destino = partida.laberinto.vecinos_accesibles(partida.jugador)[0]

    assert partida.mover_jugador((destino[0], destino[1]))
    assert partida.estado == "APARECE_FANTASMA"
    assert partida.pasos_restantes == 0
    posicion = partida.jugador
    assert not partida.mover_jugador((0, 1))
    assert partida.jugador == posicion
    assert partida.fantasma is not None


def test_enter_termina_turno_tras_dos_movimientos(registros):
    partida, _ = nueva_partida(registros, [5])
    completar_tirada_jugador(partida)
    distancias = partida.laberinto.distancias_desde((0, 0))
    primera = next(c for c in partida.laberinto.vecinos_accesibles((0, 0))
                   if distancias[c] == 1)
    segunda = next(c for c in partida.laberinto.vecinos_accesibles(primera)
                   if distancias[c] == 2)

    assert partida.mover_jugador(primera)
    assert partida.mover_jugador((segunda[0] - primera[0], segunda[1] - primera[1]))
    assert partida.pasos_restantes == 3
    assert partida.terminar_turno()
    assert partida.estado == "APARECE_FANTASMA"
    assert partida.pasos_restantes == 0


def test_aparicion_segura_en_diez_mil_posiciones_jugador(registros):
    partida, azar = nueva_partida(registros)
    laberinto = partida.laberinto
    casillas = [(c, f) for f in range(15) for c in range(15)]

    for _ in range(10_000):
        partida.jugador = azar.choice(casillas)
        partida.estado = "JUGADOR_MOVER"
        partida.fantasma = None
        partida.terminar_turno()

        assert partida.fantasma != (14, 14)
        assert laberinto.distancias_desde(partida.jugador)[partida.fantasma] >= 6


def test_llegar_a_la_meta_gana_aunque_queden_pasos(registros):
    from fantasma_ia import buscar_camino

    partida, _ = nueva_partida(registros)
    camino = buscar_camino(partida.laberinto, (0, 0), (14, 14))
    anterior = camino[-2]
    partida.jugador = anterior
    partida.estado = "JUGADOR_MOVER"
    partida.pasos_restantes = 3

    assert partida.mover_jugador((14 - anterior[0], 14 - anterior[1]))
    assert partida.estado == "VICTORIA"
    assert partida.jugador == (14, 14)
    assert partida.pasos_restantes == 2


def test_entrar_a_la_casilla_del_fantasma_pierde(registros):
    partida, _ = nueva_partida(registros)
    destino = partida.laberinto.vecinos_accesibles((0, 0))[0]
    partida.jugador = (0, 0)
    partida.fantasma = destino
    partida.estado = "JUGADOR_MOVER"
    partida.pasos_restantes = 2

    assert partida.mover_jugador((destino[0], destino[1]))
    assert partida.estado == "DERROTA"
    assert partida.jugador == partida.fantasma


def test_fantasma_captura_en_el_tercer_paso_de_un_dado_de_cinco(registros):
    partida, _ = nueva_partida(registros, [5])
    origen = (0, 0)
    distancias = partida.laberinto.distancias_desde(origen)
    jugador = next(c for c, pasos in distancias.items() if pasos == 3)
    partida.jugador = jugador
    partida.fantasma = origen
    partida.estado = "FANTASMA_TIRAR"
    partida.tirar_dado_fantasma()
    partida.dado_fantasma.actualizar(0.6)
    partida.completar_dado()
    partida.completar_busqueda()

    assert partida.estado == "FANTASMA_MOVER"
    assert partida.avanzar_fantasma()
    assert partida.estado == "FANTASMA_MOVER"
    assert partida.avanzar_fantasma()
    assert partida.estado == "FANTASMA_MOVER"
    assert partida.avanzar_fantasma()
    assert partida.estado == "DERROTA"
    assert partida.fantasma == jugador


def test_fantasma_avanza_solo_los_cuatro_pasos_del_dado(registros):
    partida, _ = nueva_partida(registros, [4])
    origen = (0, 0)
    destino = next(
        casilla for casilla, pasos in partida.laberinto.distancias_desde(origen).items()
        if pasos == 8
    )
    partida.jugador = destino
    partida.fantasma = origen
    partida.estado = "FANTASMA_TIRAR"
    partida.tirar_dado_fantasma()
    partida.dado_fantasma.actualizar(0.6)
    partida.completar_dado()
    partida.completar_busqueda()

    for _ in range(4):
        assert partida.avanzar_fantasma()

    assert partida.estado == "JUGADOR_TIRAR"
    assert partida.fantasma == partida.camino_fantasma[3]
    assert partida.fantasma != destino
    assert partida.turno == 2


def test_reiniciar_limpia_la_partida_y_conserva_el_mapa(registros):
    partida, _ = nueva_partida(registros)
    mapa = partida.laberinto
    partida.jugador = (14, 14)
    partida.fantasma = (4, 4)
    partida.turno = 5
    partida.camino_fantasma = [(4, 4), (5, 4)]
    partida.traza_fantasma = ["marca"]
    partida.estado = "VICTORIA"

    partida.reiniciar()

    assert partida.laberinto is mapa
    assert partida.estado == "JUGADOR_TIRAR"
    assert partida.turno == 1
    assert partida.jugador == (0, 0)
    assert partida.fantasma is None
    assert partida.camino_fantasma == []
    assert partida.traza_fantasma == []
