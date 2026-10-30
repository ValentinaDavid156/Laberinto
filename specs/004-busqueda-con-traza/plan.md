# Plan de implementación: búsqueda con traza

## Alcance

Implementar `fantasma_ia.py` según `spec.md`: una búsqueda determinista con pila explícita, eventos inmutables y una función abreviada que devuelve solo el camino. El módulo no importa pygame.

El laberinto lo aporta `laberinto.py`; no se modifica ese archivo ni `base/`. La búsqueda visita vecinos en el orden arriba, derecha, abajo, izquierda.

## Diseño

- `Evento` será una tupla con nombre con `tipo`, `casilla` y copia inmutable de la pila posterior al evento.
- `buscar_camino_con_traza` apilará el origen, marcará casillas visitadas al descubrirlas y emitirá `desapilar` al agotar las salidas de una casilla.
- Al alcanzar el destino emitirá `encontrado` y devolverá la pila sin el origen como camino.
- `buscar_camino` delegará en la búsqueda con traza.
- Un destino inalcanzable producirá `ValueError`.

## Secuencia TDD

1. Añadir primero pruebas unitarias de camino, traza, determinismo, retrocesos y errores; ejecutarlas y confirmar que fallan por falta del módulo.
2. Implementar el código mínimo que haga pasar esas pruebas.
3. Ejecutar la suite completa, medir cobertura de cada módulo de lógica y registrar los comandos y resultados en `validacion.md`.

## Dependencias

La funcionalidad depende del modelo existente `Laberinto` de la especificación 001. No requiere Pygame. La dependencia de ejecución del juego se declara aparte en `requirements.txt`.
