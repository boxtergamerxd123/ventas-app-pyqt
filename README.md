# Panel de Gráficas de Ventas

Aplicación de escritorio en **Python + PyQt5** para registrar y visualizar ventas por **día, mes y año**.  
El sistema guarda los registros en un archivo `ventasdiarias.txt` y permite añadir, eliminar y graficar la información de manera visual.

## Características

- Interfaz gráfica en **modo blanco** con estilo personalizado.
- Registro de ventas con fecha, hora y cantidad.
- Visualización de ventas en gráficas:
  - **Por día** (horas del día seleccionado).
  - **Por mes** (ventas acumuladas por día).
  - **Por año** (ventas acumuladas por mes).
- Posibilidad de editar o borrar registros.
- Archivo persistente `ventasdiarias.txt` (formato CSV simple).

## Requisitos

- Python 3.10+  
- Librerías necesarias (instalarlas con `pip install -r requirements.txt`):

