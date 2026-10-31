# El Laberinto del Fantasma

Juego de mesa para una persona. Cruza el laberinto mientras el fantasma busca tu rastro con backtracking. El mapa fijo es el laberinto 4 del catálogo.

## Requisitos

- Windows 10 u 11
- Python 3.12 o 3.13

## Instalación

Abre PowerShell en la carpeta del proyecto y ejecuta:

```powershell
py -3.13 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt -r requirements-dev.txt
```

Si instalaste Python 3.12, cambia `py -3.13` por `py -3.12`.

## Jugar

```powershell
.\.venv\Scripts\python.exe main.py
```

Puedes pasar una semilla entera para repetir una partida:

```powershell
.\.venv\Scripts\python.exe main.py --semilla 42
```

En el menú, `V` activa o desactiva la explicación del backtracking y `ENTER` comienza. Durante la partida, `ESPACIO` tira el dado, las flechas mueven al jugador y `ENTER` termina el turno antes de tiempo. Durante la búsqueda del fantasma, `P` pausa, `N` avanza un evento, `S` salta al final y `+` / `-` cambian la velocidad. `ESC` vuelve al menú; en el menú, `ESC` cierra el juego. En el resultado, `R` reinicia y `M` o `ESC` vuelven al menú.

## Pruebas

```powershell
.\.venv\Scripts\python.exe -m pytest --cov=laberinto --cov=fantasma_ia --cov=visualizador --cov=dado --cov=juego --cov-report=term-missing --cov-fail-under=80
```
