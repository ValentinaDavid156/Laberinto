"""Pruebas de tiradas reproducibles y animación del dado."""

import random


class FuenteVisual:
    def __init__(self):
        self.llamadas = 0

    def randint(self, minimo, maximo):
        self.llamadas += 1
        return minimo + (self.llamadas - 1) % (maximo - minimo + 1)


def test_tirada_valida_y_resultado_fijo():
    from dado import Dado

    dado = Dado(random.Random(12), FuenteVisual())
    valor = dado.tirar()

    assert 1 <= valor <= 6
    assert dado.valor == valor
    assert dado.animando
    dado.actualizar(0.6)
    assert not dado.animando
    assert dado.cara_visible == valor


def test_dado_usa_una_fuente_visual_por_defecto():
    from dado import Dado

    dado = Dado(random.Random(5))
    valor = dado.tirar()
    dado.actualizar(0.6)

    assert 1 <= valor <= 6
    assert dado.cara_visible == valor


def test_actualizar_sin_tirada_no_cambia_el_dado():
    from dado import Dado

    dado = Dado(random.Random(5), FuenteVisual())
    dado.actualizar(0.6)

    assert dado.valor is None
    assert dado.cara_visible is None
    assert not dado.animando


def test_diez_mil_tiradas_incluyen_las_seis_caras():
    from dado import Dado

    dado = Dado(random.Random(27), random.Random(8))
    resultados = {dado.tirar()}
    dado.actualizar(0.6)
    for _ in range(9_999):
        resultados.add(dado.tirar())
        dado.actualizar(0.6)

    assert resultados == {1, 2, 3, 4, 5, 6}


def test_tiradas_repetidas_durante_animacion_no_consumen_azar_logico():
    from dado import Dado

    rnd_esperado = random.Random(123)
    primero, segundo = rnd_esperado.randint(1, 6), rnd_esperado.randint(1, 6)
    dado = Dado(random.Random(123), FuenteVisual())

    assert dado.tirar() == primero
    assert dado.tirar() == primero
    dado.actualizar(0.6)
    assert dado.tirar() == segundo


def test_cambiar_frecuencia_de_actualizacion_no_cambia_las_tiradas():
    from dado import Dado

    dado_rapido = Dado(random.Random(456), random.Random(11))
    dado_lento = Dado(random.Random(456), random.Random(99))

    for _ in range(20):
        valor_rapido = dado_rapido.tirar()
        for _ in range(10):
            dado_rapido.actualizar(0.06)
        valor_lento = dado_lento.tirar()
        for _ in range(20):
            dado_lento.actualizar(0.03)
        assert valor_rapido == valor_lento


def test_cara_visual_cambia_cada_seis_centesimas_y_finaliza():
    from dado import Dado

    visual = FuenteVisual()
    dado = Dado(random.Random(8), visual)
    valor = dado.tirar()

    assert visual.llamadas == 1
    assert dado.cara_visible == 1
    dado.actualizar(0.059)
    assert visual.llamadas == 1
    dado.actualizar(0.002)
    assert visual.llamadas == 2
    dado.actualizar(0.6)
    assert visual.llamadas == 10
    assert not dado.animando
    assert dado.cara_visible == valor


def test_actualizacion_negativa_no_acelera_la_animacion():
    from dado import Dado

    dado = Dado(random.Random(8), FuenteVisual())
    dado.tirar()
    dado.actualizar(-1)

    assert dado.animando
    dado.actualizar(0.61)
    assert not dado.animando
