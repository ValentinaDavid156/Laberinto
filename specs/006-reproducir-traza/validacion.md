# Validación: reproducción de la traza

## Preparación

- Entorno final: Windows, Python 3.13.16, Pygame 2.6.1, `.venv`; el estado rojo inicial se ejecutó en Python 3.14.7 antes de instalar 3.13.
- Suite completa antes de esta funcionalidad: **256 passed in 8.70s** (Python 3.14.7).

## Estado

- Rojo, antes de implementar: `python -m pytest tests/test_visualizador.py -q` → **8 failed**, todos por `ModuleNotFoundError: No module named 'visualizador'` (Python 3.14.7).
- Verde focalizado: `python -m pytest tests/test_visualizador.py -q` → **8 passed in 0.03s**.
- Suite y cobertura (incluye las pruebas visuales): `SDL_VIDEODRIVER=dummy python -m pytest --cov=laberinto --cov=fantasma_ia --cov=visualizador --cov=dado --cov=juego --cov-report=term-missing --cov-fail-under=80 -q` → **268 passed in 21.42s**; todos los módulos de lógica superan 80 %.
- Verificación de dependencia: `.venv\Scripts\python.exe -c "import visualizador; print('pygame' in visualizador.__dict__)"` → **False**; no importa pygame.
- Decisión aplicada: intervalo `max(0.03, 4/eventos)` por evento, sin límite de duración total; `saltar()` completa inmediatamente.
- La lógica no debe importar pygame.
