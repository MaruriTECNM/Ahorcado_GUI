Codigo para la generación de un juego de Ahorcado con interfaz gráfica.

# Building Requirements #

Se necesitan los modulos PyInstaller, PyQt5, y Numpy.
En el repositorio esta el mismo archivo de requirements.txt que fue creado en base a mi .venv.

Para instalar los requisitos solo hace falta invocar a pip y escribir: `pip install -r requirements.txt`, esto invocara a pip que instalara los paqueres necesarios para la ejecución del código.

# Building #

Empezar el .venv, y después se contruye usando
`PyInstaller --onefile -w Ahorcado_GUI.py`, alternativemente se puede ejecutar el archivo .py tal cual.
