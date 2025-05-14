=============================================
PLATAFORMA DE INTEGRACIÓN DE BASES DE DATOS
=============================================

📅 Fecha: Mayo 2025
🎓 Autor: Fernando Luque Villacorta
🛠 Proyecto: Plataforma para conexión, exploración e integración de BDs heterogéneas
🗂 Tecnología: Python + Streamlit + SQLAlchemy

---------------------------------------------
🚀 ¿CÓMO EJECUTAR LA APLICACIÓN?
---------------------------------------------

1. Asegúrese de tener todos los motores de base de datos instalados (PostgreSQL, MySQL, Oracle, SQL Server, SQLite).
2. Verifique que las bases de datos de prueba se encuentren en la carpeta BDs_Prueba.
3. Active el entorno virtual con las dependencias ya instaladas.

4. Para ejecutar la aplicación:
   ➤ Haga doble clic sobre el archivo:
       📁 iniciar_app.bat

   Esto abrirá automáticamente la plataforma en su navegador predeterminado.

---------------------------------------------
📦 ESTRUCTURA DEL PROYECTO
---------------------------------------------

📁 Producto
├── app.py                 → Archivo principal de la plataforma
├── iniciar_app.bat        → Script para lanzar la aplicación sin usar consola
├── BDs_Prueba             → Contiene bases de datos en SQLite y scripts de importación
├── models.py              → Declaraciones de modelos base SQLAlchemy
├── db_utils.py            → Funciones de exportación de datos
├── insert_data.py         → Scripts para insertar datos en las BDs
├── crear_sqlite.py        → Script para crear BD SQLite desde CSV
├── usuarios_sqlite.csv    → Fuente de datos demo
├── config.py              → Variables de entorno
├── main.py                → Alternativa de ejecución
└── requirements.txt       → Lista de librerías necesarias (opcional)

---------------------------------------------
📌 NOTAS FINALES
---------------------------------------------

- Este sistema fue desarrollado como parte de un proyecto académico de integración de datos.
- Para fines de demostración, se sugiere tener los motores SQL levantados previamente.
- No se requiere ejecutar comandos en consola: solo abrir el archivo .bat.

