# Validación: dados reproducibles

## Preparación de la base

- Entorno: Windows, Python 3.14.7.
- Comando: `.venv\Scripts\python.exe -m pytest -q --cov=laberinto --cov=fantasma_ia --cov-report=term-missing --cov-fail-under=80`.
- Resultado observado al cerrar 004: **238 passed in 1.82s**; `laberinto.py` y `fantasma_ia.py` con 100 % de cobertura.

## Estado de esta funcionalidad

- Comando rojo antes de crear `dado.py`: `.venv\Scripts\python.exe -m pytest tests\test_dado.py -q` — **6 failed in 0.14s**, todos con `ModuleNotFoundError: No module named 'dado'`.
- Comando focalizado tras implementar: `.venv\Scripts\python.exe -m pytest tests\test_dado.py -q` — **8 passed in 0.07s**.
- Suite completa y cobertura: `.venv\Scripts\python.exe -m pytest -q --cov=laberinto --cov=fantasma_ia --cov=dado --cov-report=term-missing --cov-fail-under=80` — **246 passed in 1.80s**; los tres módulos de lógica tienen 100 % de cobertura.
- Reproducibilidad entre frecuencias: `test_cambiar_frecuencia_de_actualizacion_no_cambia_las_tiradas` aprobó con la misma semilla y distinta segmentación del tiempo.
- Separación gráfica: `.venv\Scripts\python.exe -S -c "import dado, sys; assert 'pygame' not in sys.modules"` — aprobado.
- CA-16 integrado con aparición y comparación real de 30/60 FPS se validará al integrar `juego.py` y `main.py`.
