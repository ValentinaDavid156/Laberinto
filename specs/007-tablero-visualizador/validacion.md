# Validación: tablero y dibujo

## Entorno y resultados

- Windows, Python 3.13.16, Pygame 2.6.1 (SDL 2.28.4).
- Pruebas primero: `python -m pytest tests/test_dibujo.py -q` → **3 failed**, `ModuleNotFoundError: No module named 'dibujo'`.
- Primera implementación: pasaron las 3 pruebas gráficas. La nueva prueba del grosor de pared encontró que las celdas tapaban dos píxeles; se cambió el orden para dibujar las paredes después de rellenar las casillas.
- Verde focalizado: `SDL_VIDEODRIVER=dummy python -m pytest tests/test_visualizador.py tests/test_dibujo.py -q` → **12 passed in 0.36s**.
- Suite y cobertura: `SDL_VIDEODRIVER=dummy python -m pytest --cov=laberinto --cov=fantasma_ia --cov=visualizador --cov=dado --cov=juego --cov-report=term-missing --cov-fail-under=80 -q` → **268 passed in 21.42s**; cobertura total 95.16 %. `juego.py` 90 %, `visualizador.py` 93 %; los demás módulos lógicos 100 %.
- Captura SDL dummy: [captura.png](captura.png), tablero 920×740, mapa 4, camino de 21 pasos, traza de 51 eventos. Revisión visual realizada: tablero, entrada, meta, actores, marcas y pila visibles; el tarro muestra 19 casillas y `… +3 más`.
- Paredes de 4 px y ventana lógica de 920×740 comprobadas en pruebas de superficie. No se abrió una ventana real todavía.
