# Prueba de corridas arriba/abajo de la media

Este pequeño script ejecuta la prueba de corridas arriba/abajo de la media
a partir de un archivo CSV local y muestra los resultados en consola con
validación final de la hipótesis.

## Archivos
- `runs_test.py`: ejecuta la prueba leyendo un archivo CSV ubicado en el
  mismo directorio. Incluye manejo de errores, cálculos estadísticos y
  salida en tablas de texto.
- `datos_corridas.csv`: archivo de ejemplo con la columna `valor`. Puedes
  reemplazarlo por tus propios datos manteniendo el encabezado.

## Uso
1. Asegúrate de tener Python 3 instalado.
2. Ubica tus datos en `datos_corridas.csv` junto al script, con una columna
   llamada `valor` que contenga valores numéricos.
3. Ejecuta en la terminal desde este directorio:

   ```bash
   python runs_test.py
   ```

El programa mostrará un resumen de los datos, los valores calculados de la
prueba y una validación indicando si la secuencia cumple o no con la
hipótesis de aleatoriedad a un nivel de significancia del 5%.
