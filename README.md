  Panel de Gráficas de Ventas

Aplicación de escritorio en Python + PyQt5 para registrar y visualizar ventas por día, mes y año.
El sistema guarda los registros en un archivo ventasdiarias.txt y permite añadir, eliminar y graficar la información de manera visual.

  Características

  Interfaz gráfica con estilo personalizado (modo claro).

  Registro de ventas con fecha, hora y cantidad.

  Visualización de gráficas:

Por día → ventas por hora.

Por mes → ventas acumuladas por día.

Por año → ventas acumuladas por mes.

  Edición y eliminación de registros directamente desde la interfaz.

  Persistencia de datos en ventasdiarias.txt (formato CSV simple).

 
  Requisitos

Python 3.10+

Librerías necesarias (instalación automática con requirements.txt):

PyQt5==5.15.9
matplotlib==3.7.1
pandas==2.0.3

 Instalación y uso

Clona el repositorio e instala las dependencias:

git clone https://github.com/boxtergamerxd123/ventas-app-pyqt
cd ventas-app-pyqt
pip install -r requirements.txt


Ejecuta la aplicación:

python graficacion.py

  Archivos

graficacion.py → archivo principal con la aplicación.

ventasdiarias.txt → archivo CSV simple donde se guardan los registros.

Se genera automáticamente si no existe.

Formato de columnas: fecha,hora,ventas.

  Mejoras futuras

Migración a base de datos SQLite en lugar de archivo CSV.

Exportar reportes a Excel/PDF.

Validaciones avanzadas de fecha y hora.

Temas personalizables (oscuro/claro).

  Licencia

Este proyecto está bajo la licencia Apache-2.0
.

Desarrollado por @boxtergamerxd123
