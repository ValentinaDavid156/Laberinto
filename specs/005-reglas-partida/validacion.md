# Validación: reglas de partida

## Preparación de la base

- Entorno: Windows, Python 3.14.7.
- Suite completa al cerrar el dado: **246 passed in 1.80s**; `laberinto.py`, `fantasma_ia.py` y `dado.py` con 100 % de cobertura.
- Mapa de juego elegido por decisión del usuario: laberinto 4 (`arbol_binario`), 28 pasos de `(0,0)` a `(14,14)`.

## Estado de esta funcionalidad

- Comando rojo antes de crear `juego.py`: `.venv\Scripts\python.exe -m pytest tests\test_juego.py -q` — **9 failed in 0.23s**, todos con `ModuleNotFoundError: No module named 'juego'`.
- Comando focalizado tras implementar: `.venv\Scripts\python.exe -m pytest tests\test_juego.py -q` — **10 passed in 5.77s**.
- Suite completa y cobertura: `.venv\Scripts\python.exe -m pytest -q --cov=laberinto --cov=fantasma_ia --cov=dado --cov=juego --cov-report=term-missing --cov-fail-under=80` — **256 passed in 8.70s**; `juego.py` 90 %, los demás módulos de lógica 100 %.
- Aparición: el caso automatizado realizó **10 000** elecciones desde posiciones aleatorias del mapa 4; ninguna cayó a menos de seis pasos ni en la meta.
- Separación gráfica: `.venv\Scripts\python.exe -S -c "import juego, sys; assert 'pygame' not in sys.modules"` — aprobado.
- El reloj permanece fuera de `Partida`; la interfaz completa animaciones mediante órdenes explícitas.
- Decisión aplicada: usar el mapa fijo 4 y omitir la spec 002. Su distancia de entrada a meta es 28 pasos.
- La comprobación visual y la prueba integrada CA-16 a 30/60 FPS quedan para la integración con `main.py`.
