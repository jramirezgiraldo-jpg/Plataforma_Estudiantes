# Plataforma Estudiantes (Educativa 2026)

Una plataforma web interactiva construida en **Python y Flask** diseñada para organizar y mostrar los materiales de estudio para estudiantes de grado 6 a 11. Cada grado tiene contenido personalizado, como Presentaciones y Mini-Juegos Interactivos.

## Funcionalidades
1. **Registro de Estudiantes**: Cada estudiante se puede registrar indicando su nombre, grado escolar y un usuario.
2. **Dashboard del Estudiante**: Interfaz gamificada con material didáctico. Contiene un sistema de progreso y experiencia por niveles (Tortuga, Búho, Zorro, Tigre, Águila) dependiendo de las actividades completadas.
3. **Dashboard del Docente (Admin)**: Tablero de posiciones visual que evalúa el avance interactivo en tiempo real y permite filtrar por cada grado escolar.
4. **Almacenamiento Local de Actividades**: Todo el contenido se inyecta directamente como HTML de la respectiva carpeta de guías. 

## Requisitos Previos
Debes contar con Python instalado y el entorno general de las librerías activas en el proyecto `Flask`.

## Instalación & Ejecución
1. Descarga el repositorio o clónalo localmente:
   ```bash
   git clone <URL_DEL_REPOSITORIO>
   cd Plataforma_Estudiantes
   ```
2. Instala Flask y Werkzeug (si usas un entorno virtual, actívalo antes):
   ```bash
   pip install Flask Werkzeug
   ```
3. Ejecutar y abrir el App localmente:
   ```bash
   python app.py
   ```
   Abre el navegador en [http://127.0.0.1:3000](http://127.0.0.1:3000)

## Estructura de Proyecto
* `app.py`: Archivo de la lógica del servidor y gestión de base de datos sqlite.
* `users.db`: Base de datos SQLite *(generada automáticamente)*.
* `templates/`: Plantillas visuales en HTML utilizando Jinja para variables e `extends base.html` como marco estético general.
* `static/styles.css`: Modificaciones de CSS orientadas al Glassmorphism, animaciones interactivas de recompensas y estilos responsivos.
