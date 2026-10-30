# Validación: búsqueda con traza

## Preparación de la base

- Entorno: Windows, Python 3.14.7.
- Comando: `.venv\Scripts\python.exe -m pytest -q`
- Resultado observado antes de añadir implementación: **233 passed in 1.95s**.
- Dependencias instaladas con `.venv\Scripts\python.exe -m pip install -r requirements-dev.txt`: pytest 8.4.2 y pytest-cov 7.0.0.

## Estado de esta funcionalidad

- La búsqueda y sus pruebas todavía no se han añadido; no se declara implementada ni validada.
- Comandos pendientes tras su implementación: `.venv\Scripts\python.exe -m pytest tests\test_fantasma_ia.py -q` y `.venv\Scripts\python.exe -m pytest -q --cov=laberinto --cov=fantasma_ia --cov-report=term-missing`.
