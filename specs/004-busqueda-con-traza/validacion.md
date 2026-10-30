# Validación: búsqueda con traza

## Preparación de la base

- Entorno: Windows, Python 3.14.7.
- Comando: `.venv\Scripts\python.exe -m pytest -q`
- Resultado observado antes de añadir implementación: **233 passed in 1.95s**.
- Dependencias instaladas con `.venv\Scripts\python.exe -m pip install -r requirements-dev.txt`: pytest 8.4.2 y pytest-cov 7.0.0.

## Estado de esta funcionalidad

- Comando rojo: `.venv\Scripts\python.exe -m pytest tests\test_fantasma_ia.py -q`.
- Resultado real antes de crear `fantasma_ia.py`: **5 failed in 0.18s**, todos con `ModuleNotFoundError: No module named 'fantasma_ia'`. Es el fallo esperado de TDD.
- En la entrega de pruebas, `fantasma_ia.py` aún no forma parte del historial; queda registrada la falla inicial previa a su implementación.
