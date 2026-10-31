"""Pruebas de integración de la aplicación con el reloj controlado."""

import pygame
import pytest


def test_menu_activa_visualizador_y_empieza_con_mapa_fijo():
    from main import Aplicacion

    aplicacion = Aplicacion(semilla=7)

    assert aplicacion.pantalla == "MENU"
    assert aplicacion.visualizador_activado
    aplicacion.manejar_tecla(pygame.K_v)
    assert not aplicacion.visualizador_activado
    aplicacion.manejar_tecla(pygame.K_RETURN)

    assert aplicacion.pantalla == "JUEGO"
    assert aplicacion.mapa_id == 4
    assert aplicacion.partida.jugador == (0, 0)


def test_teclas_mueven_y_terminan_el_turno():
    from main import Aplicacion

    aplicacion = Aplicacion(semilla=11)
    aplicacion.manejar_tecla(pygame.K_RETURN)
    aplicacion.manejar_tecla(pygame.K_SPACE)
    _hasta_estado(aplicacion, aplicacion.partida.JUGADOR_MOVER, 60)
    anterior = aplicacion.partida.jugador
    vecino = aplicacion.partida.laberinto.vecinos_accesibles(anterior)[0]
    tecla = {
        (0, -1): pygame.K_UP,
        (1, 0): pygame.K_RIGHT,
        (0, 1): pygame.K_DOWN,
        (-1, 0): pygame.K_LEFT,
    }[(vecino[0] - anterior[0], vecino[1] - anterior[1])]
    aplicacion.manejar_tecla(tecla)

    assert aplicacion.partida.jugador == vecino
    aplicacion.manejar_tecla(pygame.K_RETURN)
    assert aplicacion.partida.estado == aplicacion.partida.APARECE_FANTASMA
    assert aplicacion.partida.fantasma is not None


def test_escape_abandona_partida_y_las_pantallas_finales():
    from main import Aplicacion

    aplicacion = Aplicacion(semilla=3)
    aplicacion.manejar_tecla(pygame.K_RETURN)
    aplicacion.manejar_tecla(pygame.K_ESCAPE)
    assert aplicacion.pantalla == "MENU"

    aplicacion.manejar_tecla(pygame.K_RETURN)
    aplicacion.partida.estado = aplicacion.partida.VICTORIA
    aplicacion.manejar_tecla(pygame.K_ESCAPE)
    assert aplicacion.pantalla == "MENU"


def test_reiniciar_y_volver_al_menu_desde_resultado():
    from main import Aplicacion

    aplicacion = Aplicacion(semilla=5)
    aplicacion.manejar_tecla(pygame.K_RETURN)
    aplicacion.partida.estado = aplicacion.partida.DERROTA
    aplicacion.manejar_tecla(pygame.K_r)
    assert aplicacion.pantalla == "JUEGO"
    assert aplicacion.partida.estado == aplicacion.partida.JUGADOR_TIRAR

    aplicacion.partida.estado = aplicacion.partida.DERROTA
    aplicacion.manejar_tecla(pygame.K_m)
    assert aplicacion.pantalla == "MENU"


def test_misma_semilla_da_mismos_dados_y_aparicion_a_60_y_30_fps():
    from main import Aplicacion

    resultado_60 = _datos_de_aparicion(Aplicacion(semilla=2026), 60)
    resultado_30 = _datos_de_aparicion(Aplicacion(semilla=2026), 30)

    assert resultado_60 == resultado_30


def test_render_menu_y_partida_en_superficie_dummy():
    from main import Aplicacion

    pygame.init()
    aplicacion = Aplicacion(semilla=1)
    superficie = pygame.Surface((920, 740))
    aplicacion.dibujar(superficie)
    aplicacion.manejar_tecla(pygame.K_RETURN)
    aplicacion.dibujar(superficie)

    assert superficie.get_size() == (920, 740)
    assert superficie.get_at((10, 10))[:3] == (255, 255, 255)


def test_controles_de_traza_y_avance_del_fantasma():
    from main import Aplicacion

    aplicacion = Aplicacion(semilla=42)
    _llegar_a_busqueda(aplicacion)
    aplicacion.manejar_tecla(pygame.K_p)
    aplicacion.actualizar(1.0)
    assert aplicacion.reproductor.indice == 0

    aplicacion.manejar_tecla(pygame.K_n)
    assert aplicacion.reproductor.indice == 1
    aplicacion.manejar_tecla(pygame.K_s)
    aplicacion.actualizar(0.5)

    assert aplicacion.partida.estado == aplicacion.partida.FANTASMA_MOVER


def test_visualizador_desactivado_pasa_directo_a_mover_fantasma():
    from main import Aplicacion

    aplicacion = Aplicacion(semilla=42)
    aplicacion.manejar_tecla(pygame.K_v)
    _llegar_a_busqueda(aplicacion)
    aplicacion.actualizar(0)

    assert aplicacion.reproductor.terminado
    assert aplicacion.partida.estado == aplicacion.partida.FANTASMA_MOVER


def test_semilla_no_entera_se_rechaza(capsys):
    from main import crear_parser

    with pytest.raises(SystemExit):
        crear_parser().parse_args(["--semilla", "abc"])
    assert "la semilla debe ser un número entero" in capsys.readouterr().err


def _hasta_estado(aplicacion, estado, fps):
    for _ in range(fps * 3):
        if aplicacion.partida.estado == estado:
            return
        aplicacion.actualizar(1 / fps)
    raise AssertionError("La partida no alcanzó el estado esperado.")


def _llegar_a_busqueda(aplicacion, fps=60):
    aplicacion.manejar_tecla(pygame.K_RETURN)
    aplicacion.manejar_tecla(pygame.K_SPACE)
    _hasta_estado(aplicacion, aplicacion.partida.JUGADOR_MOVER, fps)
    aplicacion.manejar_tecla(pygame.K_RETURN)
    _hasta_estado(aplicacion, aplicacion.partida.DADO_FANTASMA, fps)
    _hasta_estado(aplicacion, aplicacion.partida.FANTASMA_BUSCA, fps)


def _datos_de_aparicion(aplicacion, fps):
    aplicacion.manejar_tecla(pygame.K_RETURN)
    aplicacion.manejar_tecla(pygame.K_SPACE)
    _hasta_estado(aplicacion, aplicacion.partida.JUGADOR_MOVER, fps)
    dado_jugador = aplicacion.partida.dado_jugador.valor
    aplicacion.manejar_tecla(pygame.K_RETURN)
    fantasma = aplicacion.partida.fantasma
    _hasta_estado(aplicacion, aplicacion.partida.DADO_FANTASMA, fps)
    dado_fantasma = aplicacion.partida.dado_fantasma.valor
    return dado_jugador, fantasma, dado_fantasma
