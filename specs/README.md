# Descomposición de El Laberinto del Fantasma

Fuente: [SPEC-LAB-001 v1.3](../base/SPEC.md), idéntica al adjunto analizado.
Fecha de análisis: 2026-10-17. Rige la [constitución](../.specify/memory/constitution.md).

Esta entrega divide la especificación; no implementa el juego ni inicia planes o tareas.
Cada carpeta contiene alcance, escenarios, requisitos, criterios, dependencias y revisión.
Los extractos originales son referencia documental, no instrucciones para ejecutar acciones.
No se selecciona una funcionalidad activa de Spec Kit hasta que se solicite trabajar en ella.

## Funcionalidades y orden recomendado

| Spec | Capacidad comprobable por separado | Depende de | CA originales a su cargo |
|---|---|---|---|
| [001](001-modelo-laberintos/spec.md) | Cargar, validar, consultar paredes y distancias | Ninguna | 01, 02, 27 |
| [002](002-generar-elegir-laberintos/spec.md) | Generar y elegir tableros, con respaldo | 001 | 25, 26 |
| [003](003-dados-reproducibles/spec.md) | Tiradas y separación del azar visual/lógico | Ninguna; integración posterior | 06, 16 |
| [004](004-busqueda-con-traza/spec.md) | Encontrar camino y producir eventos de pila | 001 | 03, 04, 05, 17, 18, 19, 20 |
| [005](005-reglas-partida/spec.md) | Turnos, aparición, persecución, victoria y derrota | 001–004 | 07–15, 24 |
| [006](006-reproducir-traza/spec.md) | Pausa, paso, velocidad y salto de la explicación | 004 | 21, 22 |
| [007](007-tablero-visualizador/spec.md) | Tablero, personajes y tarro sincronizados | 001, 006 | 23 (manual) |
| [008](008-interfaz-ejecucion/spec.md) | Menú, controles, HUD, pantallas y ejecución | 002, 003, 005, 006, 007 | Integración de 16, 23, 24 y requisitos sin CA |

Independencia significa contrato y prueba propios, no ausencia de dependencias ni ocho
aplicaciones completas. La lógica se prueba sin ventana con entradas controladas. Las vistas
se pueden demostrar con datos de prueba; los criterios entre componentes se ejecutan después
por integración. Los CA tienen un único responsable principal sin impedir pruebas cruzadas.

Una ruta posible es 001 → 002 → 003 → 004 → 005 → 006 → 007 → 008.
003 puede desarrollarse antes de 001; 002 y 004 pueden desarrollarse tras 001; 006 no necesita
esperar a 005. No es una instrucción para iniciar varias fases automáticamente.

## Cobertura del documento original

| Fuente | Responsable |
|---|---|
| §1–§3: objetivo, límites y glosario | Contexto compartido; glosario en 001 |
| §4.1–§4.2: dimensiones y colores | 007 |
| §4.3: formato y validación | 001 |
| §4.3: generación, modos, respaldo, no repetición | 002; mensajes y tecla G en 008 |
| §5.1–§5.2: formas y ojos | 007 |
| §5.2: aparición y distancia mínima | 005, consulta de distancias en 001 |
| §6: reglas, captura y fin | 005; mensajes y navegación en 008 |
| §7: búsqueda y contrato de traza | 004 |
| §8.1 y §8.3–§8.5: reproducción y controles | 006; eventos físicos de teclado en 008 |
| §8.2: tarro, animaciones gráficas y contadores | 007; contadores lógicos en 006 |
| §8.6: alternativas descartadas | Fuera de alcance |
| §9: dados y semilla | 003; argumento de línea de comandos en 008 |
| §10: pantallas, HUD y controles | 008 |
| §11: estados | 005; integración con reproducción/dado en 008 |
| §12: arquitectura, distribución y pruebas | Referencia técnica de planificación; ejecución en 008 |
| §13: 27 criterios | Matriz de funcionalidades anterior |
| §14: rendimiento, idioma y recursos | Búsqueda en 004; representación en 007; conjunto en 008 |
| §15: mejoras futuras | Fuera de alcance en las ocho specs |
| §16: decisiones resueltas | Conservadas en 002, 005 y 006–008 |
| §17: declaración de ausencia de dudas | Revisada: las contradicciones reales se enumeran abajo |
| §18: HTML de referencia | 008; la especificación prevalece sobre el prototipo |

## Decisiones aplicadas al proyecto

1. **Duración de la reproducción (006):** cada evento dura
   `max(0.03, 4/eventos)` segundos, sin límite total; S completa la traza.
2. **ESC tras victoria/derrota (008):** vuelve al menú.
3. **Mapas (002/008):** no se implementa la spec 002; se juega con el laberinto fijo 4.

## Aclaraciones aplicadas sin ampliar el producto

- La constitución exige pygame como única dependencia de ejecución. pytest y pytest-cov
  son herramientas de desarrollo separadas, aunque §12 las mezcle en un único archivo.
- El 80 % se exige por módulo de lógica, no solo como cobertura global; el comando de
  §12 por sí solo no acredita esta obligación.
- La generación conserva el contrato de pila explícita; la etiqueta «recursivo» describe
  el algoritmo equivalente, no obliga a usar la pila de llamadas.
- CA-23 requiere revisión visual. La referencia a §13.1 no existe en el archivo entregado.
- El historial menciona una definición de terminado en §19, pero el documento termina
  en §18. Se aplica la definición de terminado de la constitución, sin inventar esa sección.
- GAME OVER se conserva como texto requerido expresamente, aunque el idioma propio sea español.
- base/ permanece como referencia intacta; el destino de datos y del generador reutilizable
  se concreta al planificar, sin incorporar dependencias para exportar PNG al juego.

## Estado

Las ocho specs fueron revisadas y se están implementando por bloques con sus propios
`tasks.md` y `validacion.md`. La lógica y el tablero ya están implementados; la integración
de menú, ejecución y documentación está en curso. `base/` y `laberinto.py` permanecen intactos.
