# Validación: interfaz y ejecución

## Entorno y resultados

- Windows, Python 3.13.16, Pygame 2.6.1 (SDL 2.28.4), SDL dummy para pruebas.
- Pruebas primero: `python -m pytest tests/test_main.py -q` → **6 failed**, todas por `ModuleNotFoundError: No module named 'main'`.
- Pruebas de aplicación tras implementar: `SDL_VIDEODRIVER=dummy python -m pytest tests/test_main.py -q` → **9 passed**.
- La prueba CA-16 controla la aplicación con `actualizar(1/60)` y `actualizar(1/30)`; para semilla 2026 coinciden el dado del jugador, la aparición del fantasma y el dado del fantasma.
- Decisiones aplicadas: mapa fijo 4, no implementar spec 002, visualizador activado por defecto y ESC desde el resultado vuelve al menú.
- Rechazo de semilla inválida: `python main.py --semilla abc` informa `la semilla debe ser un número entero`; la prueba confirma que se rechaza antes de abrir la ventana.
- Suite y cobertura: `SDL_VIDEODRIVER=dummy python -m pytest --cov=laberinto --cov=fantasma_ia --cov=visualizador --cov=dado --cov=juego --cov-report=term-missing --cov-fail-under=80 -q` → **279 passed in 22.45s**; cobertura total 97.04 %, con `juego.py` en 93 % y `visualizador.py` en 97 %; los demás módulos de lógica, 100 %.
- Smoke test del bucle: `main(['--semilla', '42'])` inició y respondió al evento de cierre en SDL dummy.
- Medición local SDL dummy, escena con búsqueda activa: **60.3 FPS** promedio en 180 cuadros durante 2.98 s. Es una medición de este equipo/entorno; no acredita otras plataformas.
- Capturas revisadas: [menú](menu.png) y [partida](captura.png), ambas de 920×740; en la partida se ven el mapa 4, los dados, la búsqueda y el tarro.
- Lanzamiento interactivo: `.venv\Scripts\python.exe main.py --semilla 42`; ventana abierta y proceso Windows 22248 respondió. Queda disponible para la prueba manual de la usuaria.
