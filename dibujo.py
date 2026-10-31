"""Dibujo del tablero, los actores y la pila con primitivas de pygame."""

import pygame

import config


_fuentes = {}


def _fuente(tamano, negrita=False):
    clave = (tamano, negrita)
    if clave not in _fuentes:
        _fuentes[clave] = pygame.font.Font(None, tamano)
        _fuentes[clave].set_bold(negrita)
    return _fuentes[clave]


def bloques_visibles(pila):
    pila = tuple(pila)
    if len(pila) > 20:
        return pila[-19:], len(pila) - 19
    return pila, 0


def dibujar(superficie, partida, reproductor=None, dado_jugador=None,
            dado_fantasma=None, mensaje="", tiempo_evento=1.0,
            duracion_evento=0.12):
    superficie.fill(config.FONDO)
    _dibujar_laberinto(superficie, partida, reproductor)
    _dibujar_actores(superficie, partida)
    _dibujar_panel(superficie, reproductor, tiempo_evento, duracion_evento)
    _dibujar_hud(superficie, partida, dado_jugador, dado_fantasma, mensaje)


def dibujar_menu(superficie, visualizador_activado):
    superficie.fill(config.FONDO)
    lineas = (
        ("El Laberinto del Fantasma", 54, True, 250),
        ("Mapa fijo: laberinto 4", 30, False, 350),
        ("V: visualizador de backtracking ["
         + ("ACTIVADO" if visualizador_activado else "DESACTIVADO") + "]", 28, False, 415),
        ("ENTER para comenzar", 30, False, 490),
        ("ESC para salir", 24, False, 545),
    )
    for texto, tamano, negrita, y in lineas:
        imagen = _fuente(tamano, negrita).render(texto, True, config.TEXTO)
        superficie.blit(imagen, imagen.get_rect(center=(460, y)))


def dibujar_final(superficie, partida):
    capa = pygame.Surface(superficie.get_size(), pygame.SRCALPHA)
    capa.fill((0, 0, 0, 160))
    superficie.blit(capa, (0, 0))
    victoria = partida.estado == partida.VICTORIA
    mensaje = "¡HAS GANADO!" if victoria else "GAME OVER"
    color = (50, 230, 100) if victoria else (240, 50, 50)
    titulo = _fuente(64, True).render(mensaje, True, color)
    superficie.blit(titulo, titulo.get_rect(center=(460, 300)))
    subtitulo = _fuente(26).render(
        "Turnos: " + str(partida.turno) + "   R reinicia · M / ESC menú",
        True, config.FONDO,
    )
    superficie.blit(subtitulo, subtitulo.get_rect(center=(460, 360)))


def _dibujar_laberinto(superficie, partida, reproductor):
    laberinto = partida.laberinto
    for fila in range(config.N):
        for columna in range(config.N):
            x = config.MARGEN + columna * config.TAM_CELDA
            y = config.MARGEN + fila * config.TAM_CELDA
            casilla = (columna, fila)
            color = config.FONDO
            if reproductor is not None:
                estado = reproductor.estado_casilla(casilla)
                if estado == "camino":
                    color = config.CAMINO
                elif estado == "en_pila":
                    color = config.EN_PILA
                elif estado == "descartada":
                    color = config.DESCARTADA
            if casilla == (0, 0):
                color = config.ENTRADA
            if casilla == (14, 14):
                color = config.META
            pygame.draw.rect(superficie, color, (x, y, 40, 40))
            if casilla == (14, 14):
                texto = _fuente(16, True).render("META", True, config.TEXTO)
                superficie.blit(texto, texto.get_rect(center=(x + 20, y + 20)))

    for fila in range(config.N):
        for columna in range(config.N):
            x = config.MARGEN + columna * config.TAM_CELDA
            y = config.MARGEN + fila * config.TAM_CELDA
            if laberinto.grid[2 * fila + 1][2 * columna + 2] == "#":
                pygame.draw.rect(superficie, config.PARED, (x + 38, y, 4, 40))
            if laberinto.grid[2 * fila + 2][2 * columna + 1] == "#":
                pygame.draw.rect(superficie, config.PARED, (x, y + 38, 40, 4))

    for fila in range(config.N):
        y = config.MARGEN + fila * 40
        if fila != 0:
            pygame.draw.rect(superficie, config.PARED, (config.MARGEN - 2, y, 4, 40))
        if fila != 14:
            pygame.draw.rect(superficie, config.PARED, (618, y, 4, 40))
    for columna in range(config.N):
        x = config.MARGEN + columna * 40
        pygame.draw.rect(superficie, config.PARED, (x, config.MARGEN - 2, 40, 4))
        pygame.draw.rect(superficie, config.PARED, (x, 618, 40, 4))

    if reproductor is not None and reproductor.cima is not None:
        c, f = reproductor.cima
        pygame.draw.rect(
            superficie, config.CIMA,
            (config.MARGEN + c * 40 + 2, config.MARGEN + f * 40 + 2, 36, 36), 3,
        )


def _dibujar_actores(superficie, partida):
    x, y = _centro(partida.jugador)
    pygame.draw.circle(superficie, config.JUGADOR, (x, y), 14)
    for ojo_x in (x - 5, x + 5):
        pygame.draw.circle(superficie, (255, 255, 255), (ojo_x, y - 3), 3)
        pygame.draw.circle(superficie, config.TEXTO, (ojo_x, y - 3), 1)

    if partida.fantasma is None:
        return
    x, y = _centro(partida.fantasma)
    morado = config.FANTASMA
    pygame.draw.circle(superficie, morado, (x, y - 2), 15)
    pygame.draw.rect(superficie, morado, (x - 15, y - 2, 30, 17))
    for px in (x - 10, x, x + 10):
        pygame.draw.circle(superficie, config.FONDO, (px, y + 14), 5)
    dx, dy = partida.direccion_fantasma
    for offset in (-5, 5):
        ojo = (x + offset + dx * 2, y - 3 + dy * 2)
        pygame.draw.circle(superficie, config.FONDO, ojo, 4)
        pygame.draw.circle(superficie, config.TEXTO, ojo, 2)


def _dibujar_panel(superficie, reproductor, tiempo_evento, duracion_evento):
    pygame.draw.rect(superficie, config.FONDO, (640, 0, 280, 640))
    titulo = _fuente(24, True).render("Pila del backtracking", True, config.TEXTO)
    superficie.blit(titulo, titulo.get_rect(center=(780, 28)))
    pygame.draw.lines(
        superficie, config.TARRO, False,
        ((700, 60), (700, 500), (708, 514), (852, 514), (860, 500), (860, 60)), 3,
    )
    pygame.draw.line(superficie, config.TARRO, (690, 60), (735, 60), 5)
    pygame.draw.line(superficie, config.TARRO, (825, 60), (870, 60), 5)

    if reproductor is None or reproductor.esperando:
        texto = _fuente(20).render("Esperando al fantasma…", True, config.TEXTO)
        superficie.blit(texto, texto.get_rect(center=(780, 285)))
        return

    visibles, ocultos = bloques_visibles(reproductor.pila_visible)
    y_base = 498
    if ocultos:
        y = y_base
        _bloque(superficie, "… +" + str(ocultos) + " más", y, (220, 220, 220))
        y_base -= 22

    parpadea = reproductor.evento_actual is not None and reproductor.evento_actual.tipo == "encontrado"
    color_encontrado = config.CAMINO if int(max(0, tiempo_evento) / 0.12) % 2 == 0 else config.FONDO
    for indice, casilla in enumerate(visibles):
        y = y_base - indice * 22
        color = color_encontrado if parpadea else config.FONDO
        if (reproductor.evento_actual is not None
                and reproductor.evento_actual.tipo == "apilar"
                and indice == len(visibles) - 1):
            avance = min(1.0, max(0.0, tiempo_evento / duracion_evento))
            y = round(60 + (y - 60) * avance)
        _bloque(superficie, _texto_casilla(casilla, indice == 0 and not ocultos), y, color)
        if indice == len(visibles) - 1 and visibles:
            pygame.draw.rect(superficie, config.CIMA, (710, y, 140, 20), 3)

    evento = reproductor.evento_actual
    if (evento is not None and evento.tipo == "desapilar"
            and tiempo_evento < duracion_evento and not ocultos and len(visibles) < 20):
        avance = min(1.0, max(0.0, tiempo_evento / duracion_evento))
        y = round(58 - 42 * avance)
        rojo = (255, round(190 + 65 * avance), round(190 + 65 * avance))
        _bloque(superficie, _texto_casilla(evento.casilla, False), y, rojo)

    flecha = _fuente(18, True).render("← cima", True, config.CIMA)
    superficie.blit(flecha, (862, 75))
    lineas = (
        "Apilados: " + str(reproductor.apilados),
        "Desapilados: " + str(reproductor.desapilados),
        "Profundidad: " + str(reproductor.profundidad_actual),
        "Máxima: " + str(reproductor.profundidad_maxima),
        _mensaje_evento(reproductor.evento_actual, reproductor.camino_encontrado),
    )
    for i, linea in enumerate(lineas):
        texto = _fuente(18 if i < 4 else 16).render(linea, True, config.TEXTO)
        superficie.blit(texto, (660, 530 + i * 20))


def _bloque(superficie, etiqueta, y, color):
    rect = pygame.Rect(710, y, 140, 20)
    pygame.draw.rect(superficie, color, rect)
    pygame.draw.rect(superficie, config.TARRO, rect, 1)
    texto = _fuente(16).render(etiqueta, True, config.TEXTO)
    superficie.blit(texto, texto.get_rect(center=rect.center))


def _texto_casilla(casilla, es_inicio):
    if es_inicio:
        return "inicio"
    return "(" + str(casilla[0]) + "," + str(casilla[1]) + ")"


def _dibujar_hud(superficie, partida, dado_jugador, dado_fantasma, mensaje):
    pygame.draw.rect(superficie, (245, 245, 245), (0, 640, 920, 100))
    pygame.draw.line(superficie, config.TARRO, (0, 640), (920, 640), 2)
    estado = mensaje or _estado(partida)
    turno = _fuente(16, True).render(
        "Mapa 4 · Turno: " + str(partida.turno), True, config.TEXTO,
    )
    superficie.blit(turno, (20, 678))
    _dibujar_dado(superficie, 145, "Jugador", dado_jugador)
    _dibujar_dado(superficie, 235, "Fantasma", dado_fantasma)
    texto = _fuente(20).render(estado, True, config.TEXTO)
    superficie.blit(texto, (330, 680))


def _dibujar_dado(superficie, x, etiqueta, dado):
    titulo = _fuente(16).render(etiqueta, True, config.TEXTO)
    superficie.blit(titulo, (x, 646))
    rect = pygame.Rect(x, 665, 60, 60)
    pygame.draw.rect(superficie, config.FONDO, rect)
    pygame.draw.rect(superficie, config.TEXTO, rect, 3)
    valor = None if dado is None else (dado.cara_visible if dado.animando else dado.valor)
    if valor not in range(1, 7):
        return
    puntos = {
        1: ((1, 1),),
        2: ((0, 0), (2, 2)),
        3: ((0, 0), (1, 1), (2, 2)),
        4: ((0, 0), (2, 0), (0, 2), (2, 2)),
        5: ((0, 0), (2, 0), (1, 1), (0, 2), (2, 2)),
        6: ((0, 0), (2, 0), (0, 1), (2, 1), (0, 2), (2, 2)),
    }
    for columna, fila in puntos[valor]:
        centro = (x + 16 + columna * 14, 681 + fila * 14)
        pygame.draw.circle(superficie, config.TEXTO, centro, 4)


def _estado(partida):
    estados = {
        partida.JUGADOR_TIRAR: "Tu turno: pulsa ESPACIO para tirar",
        partida.DADO_JUGADOR: "Preparando el dado del jugador…",
        partida.JUGADOR_MOVER: "Mueve con las flechas: quedan "
        + str(partida.pasos_restantes) + " pasos · ENTER para terminar",
        partida.APARECE_FANTASMA: "¡Apareció el fantasma!",
        partida.FANTASMA_TIRAR: "Turno del fantasma",
        partida.DADO_FANTASMA: "Preparando el dado del fantasma…",
        partida.FANTASMA_BUSCA: "El fantasma busca tu rastro…",
        partida.FANTASMA_MOVER: "El fantasma avanza…",
        partida.VICTORIA: "¡HAS GANADO!",
        partida.DERROTA: "GAME OVER",
    }
    return estados.get(partida.estado, "")


def _mensaje_evento(evento, camino):
    if evento is None:
        return "Esperando…"
    c, f = evento.casilla
    if evento.tipo == "encontrado":
        return "¡Encontrado! Camino de " + str(len(camino)) + " pasos"
    if evento.tipo == "desapilar":
        return "Desapilar (" + str(c) + "," + str(f) + "): retrocedo"
    return "Apilar (" + str(c) + "," + str(f) + "): avanzo"


def _centro(casilla):
    c, f = casilla
    return (config.MARGEN + c * 40 + 20, config.MARGEN + f * 40 + 20)
