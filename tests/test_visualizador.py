"""Pruebas del reproductor puro de trazas."""

from fantasma_ia import Evento


def traza_prueba():
    origen = (0, 0)
    rama = (1, 0)
    destino = (0, 1)
    return [
        Evento("apilar", origen, (origen,)),
        Evento("apilar", rama, (origen, rama)),
        Evento("desapilar", rama, (origen,)),
        Evento("apilar", destino, (origen, destino)),
        Evento("encontrado", destino, (origen, destino)),
    ]


def test_reproductor_empieza_vacio_y_esperando():
    from visualizador import ReproductorTraza

    reproductor = ReproductorTraza()

    assert reproductor.esperando
    assert reproductor.pila_visible == ()
    assert reproductor.evento_actual is None
    assert reproductor.apilados == 0
    assert reproductor.desapilados == 0


def test_actualizar_reproduce_un_evento_y_sincroniza_contadores():
    from visualizador import ReproductorTraza

    reproductor = ReproductorTraza()
    reproductor.iniciar(traza_prueba())
    reproductor.actualizar(0.79)
    assert reproductor.indice == 0
    reproductor.actualizar(0.02)

    assert reproductor.indice == 1
    assert reproductor.evento_actual.tipo == "apilar"
    assert reproductor.pila_visible == ((0, 0),)
    assert reproductor.apilados == 1
    assert reproductor.profundidad_actual == 1
    assert reproductor.profundidad_maxima == 1


def test_pausa_bloquea_el_reloj_y_paso_avanza_un_evento():
    from visualizador import ReproductorTraza

    reproductor = ReproductorTraza()
    reproductor.iniciar(traza_prueba())
    reproductor.pausar()
    reproductor.actualizar(10)

    assert reproductor.indice == 0
    assert reproductor.avanzar_uno()
    assert reproductor.indice == 1
    assert reproductor.pila_visible == ((0, 0),)
    assert reproductor.pausado
    reproductor.pausar()
    assert not reproductor.avanzar_uno()


def test_saltar_deja_pila_marcas_camino_y_contadores_finales():
    from visualizador import ReproductorTraza

    reproductor = ReproductorTraza()
    reproductor.iniciar(traza_prueba())
    reproductor.pausar()
    reproductor.saltar()

    assert reproductor.terminado
    assert reproductor.indice == 5
    assert reproductor.evento_actual.tipo == "encontrado"
    assert reproductor.pila_visible == ((0, 0), (0, 1))
    assert reproductor.descartadas == {(1, 0)}
    assert reproductor.camino_encontrado == ((0, 1),)
    assert reproductor.estado_casilla((0, 1)) == "camino"
    assert reproductor.estado_casilla((1, 0)) == "descartada"
    assert reproductor.apilados == 3
    assert reproductor.desapilados == 1
    assert reproductor.profundidad_maxima == 2


def test_visualizador_desactivado_llega_directo_al_final():
    from visualizador import ReproductorTraza

    reproductor = ReproductorTraza(activado=False)
    reproductor.iniciar(traza_prueba())

    assert reproductor.terminado
    assert reproductor.indice == 5
    assert reproductor.camino_encontrado == ((0, 1),)


def test_velocidad_se_duplica_y_se_reduce_con_limites():
    from visualizador import ReproductorTraza

    reproductor = ReproductorTraza()
    for _ in range(4):
        reproductor.acelerar()
    assert reproductor.velocidad == 4
    reproductor.acelerar()
    assert reproductor.velocidad == 4
    for _ in range(8):
        reproductor.reducir()
    assert reproductor.velocidad == 0.25
    reproductor.reducir()
    assert reproductor.velocidad == 0.25


def test_tiempo_en_pasos_distintos_da_el_mismo_resultado():
    from visualizador import ReproductorTraza

    primera = ReproductorTraza()
    segunda = ReproductorTraza()
    primera.iniciar(traza_prueba())
    segunda.iniciar(traza_prueba())
    primera.actualizar(1.61)
    segunda.actualizar(0.4)
    segunda.actualizar(0.4)
    segunda.actualizar(0.81)

    assert primera.indice == segunda.indice == 2
    assert primera.pila_visible == segunda.pila_visible
    assert primera.apilados == segunda.apilados


def test_iniciar_traza_vacia_y_limpiar_vuelven_a_espera():
    from visualizador import ReproductorTraza

    reproductor = ReproductorTraza()
    assert not reproductor.iniciar([])
    reproductor.iniciar(traza_prueba())
    reproductor.saltar()
    reproductor.limpiar()

    assert reproductor.esperando
    assert reproductor.pila_visible == ()
    assert reproductor.indice == 0
    assert reproductor.evento_actual is None
