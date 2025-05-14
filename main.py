import pandas as pd  # Para manipular datos en formato tabular (como Excel)
from sqlalchemy import create_engine  # Para conectarse a bases de datos
from config import construir_url  # Función que genera la URL de conexión
from db_utils import obtener_usuarios  # Función que extrae usuarios desde una base

# Esta función prueba si una base de datos se puede conectar correctamente
def test_connection(db_key):
    """Prueba la conexión con una base de datos especificada por su clave."""
    try:
        engine = create_engine(construir_url(db_key))
        with engine.connect():
            print(f"✅ Conexión exitosa con {db_key}")
    except Exception as e:
        print(f"❌ Error al conectar con {db_key}: {e}")

# Obtener usuarios desde cada base de datos definida
usuarios_sqlite = obtener_usuarios("sqlite")
usuarios_postgres = obtener_usuarios("postgres")
usuarios_mysql = obtener_usuarios("mysql")
usuarios_oracle = obtener_usuarios("oracle")
usuarios_sqlserver = obtener_usuarios("sqlserver")

# Unificamos todos los usuarios en una sola lista
usuarios_totales = (
    usuarios_sqlite
    + usuarios_postgres
    + usuarios_mysql
    + usuarios_oracle
    + usuarios_sqlserver
)

# Mostramos por consola todos los usuarios unificados
print("\n📊 Usuarios unificados:")
for u in usuarios_totales:
    print(u)

# Convertimos la lista de diccionarios a un DataFrame (como una tabla de Excel)
df_usuarios = pd.DataFrame(usuarios_totales)

# Exportamos esa tabla a un archivo CSV
df_usuarios.to_csv("usuarios_unificados.csv", index=False, encoding='utf-8')
print("✅ Archivo 'usuarios_unificados.csv' generado con éxito.")

# ---------------- VALIDACIONES ----------------

# Validación 1: Revisamos si hay campos vacíos en las columnas 'nombre' o 'email'
nulos = df_usuarios[df_usuarios[['nombre', 'email']].isnull().any(axis=1)]
if not nulos.empty:
    print("\n⚠️ Advertencia: Se encontraron registros con campos nulos:")
    print(nulos)
else:
    print("\n✅ No hay campos nulos en 'nombre' o 'email'.")

# Validación 2: Detectamos si hay duplicados según combinación de ID y origen
duplicados = df_usuarios[df_usuarios.duplicated(subset=['id', 'origen'], keep=False)]
if not duplicados.empty:
    print("\n⚠️ Advertencia: Se encontraron IDs duplicados:")
    print(duplicados)
else:
    print("\n✅ No hay IDs duplicados en 'id' + 'origen'.")

# Validación 3: Verificamos que el campo 'origen' tenga valores válidos
origenes_validos = {"sqlite", "postgres", "mysql", "oracle", "sqlserver"}
origenes_invalidos = df_usuarios[~df_usuarios['origen'].isin(origenes_validos)]
if not origenes_invalidos.empty:
    print("\n⚠️ Advertencia: Se encontraron registros con 'origen' inválido:")
    print(origenes_invalidos)
else:
    print("\n✅ Todos los registros tienen un 'origen' válido.")
