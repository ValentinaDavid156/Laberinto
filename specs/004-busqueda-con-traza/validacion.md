# Validación: búsqueda con traza

## Preparación de la base

- Entorno: Windows, Python 3.14.7.
- Comando: `.venv\Scripts\python.exe -m pytest -q`
- Resultado observado antes de añadir implementación: **233 passed in 1.95s**.
- Dependencias instaladas con `.venv\Scripts\python.exe -m pip install -r requirements-dev.txt`: pytest 8.4.2 y pytest-cov 7.0.0.

## Estado de esta funcionalidad

- Comando rojo: `.venv\Scripts\python.exe -m pytest tests\test_fantasma_ia.py -q`.
- Resultado real antes de crear `fantasma_ia.py`: **5 failed in 0.18s**, todos con `ModuleNotFoundError: No module named 'fantasma_ia'`. Es el fallo esperado de TDD.
- Comando focalizado tras implementar: `.venv\Scripts\python.exe -m pytest tests\test_fantasma_ia.py -q` — **5 passed in 0.03s**.
- Suite completa y cobertura: `.venv\Scripts\python.exe -m pytest -q --cov=laberinto --cov=fantasma_ia --cov-report=term-missing --cov-fail-under=80` — **238 passed in 1.85s**; `laberinto.py` 100 %, `fantasma_ia.py` 100 %.
- Separación gráfica: `.venv\Scripts\python.exe -S -c "import fantasma_ia, sys; assert 'pygame' not in sys.modules"` — aprobado.
- Rendimiento: se seleccionó en cada mapa un par de casillas a distancia máxima y se repitió 100 veces la búsqueda con traza. Peor tiempo observado: mapa 1, **0.648 ms**; mapa 2, **0.801 ms**; mapa 3, **0.741 ms**; mapa 4, **1.065 ms**; mapa 5, **0.317 ms**. Equipo/entorno: Windows, Python 3.14.7.
- `fantasma_ia.py` no importa pygame. La comprobación visual no aplica a esta lógica sin interfaz.
