# config.py — Configuración base sin soporte para Oracle

import streamlit as st
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Usuario, Base
from db_utils import exportar_csv_unificado
from validators import validar_datos

# ------------------------------
# Variables globales
# ------------------------------
usuarios_unificados = []

# ------------------------------
# Valores por defecto por motor
# ------------------------------
defaults = {
    "sqlite":   {"host": "localhost", "puerto": "",     "usuario": "",        "clave": "",      "nombre_bd": "BDtestTipoSQLite.db"},
    "postgres": {"host": "localhost", "puerto": "5432",  "usuario": "postgres","clave": "123456","nombre_bd": "northwind"},
    "mysql":    {"host": "localhost", "puerto": "3306",  "usuario": "root",    "clave": "123456","nombre_bd": "sakila"},
    "sqlserver":{"host": "DESKTOP-9EK5NEP","puerto": "", "usuario": "",        "clave": "",      "nombre_bd": "AdventureWorks2022"}
}

# ------------------------------
# Función para construir URL por clave
# ------------------------------
def construir_url(tipo):
    d = defaults[tipo]
    if tipo == "sqlite":
        return f"sqlite:///{d['nombre_bd']}"
    elif tipo == "sqlserver":
        return f"mssql+pyodbc://@{d['host']}/{d['nombre_bd']}?driver=ODBC+Driver+17+for+SQL+Server&trusted_connection=yes"
    elif tipo == "postgres":
        return f"postgresql+psycopg2://{d['usuario']}:{d['clave']}@{d['host']}:{d['puerto']}/{d['nombre_bd']}"
    elif tipo == "mysql":
        return f"mysql+pymysql://{d['usuario']}:{d['clave']}@{d['host']}:{d['puerto']}/{d['nombre_bd']}"
    else:
        raise ValueError("Motor no soportado")

# ------------------------------
# Interfaz - Sidebar con autocompletado
# ------------------------------
st.sidebar.title("⚙️ Configuración de Conexión")

tipo_bd = st.sidebar.selectbox("Tipo de Base de Datos", list(defaults.keys()))
d = defaults[tipo_bd]

host = st.sidebar.text_input("Host", value=d["host"])
puerto = st.sidebar.text_input("Puerto", value=d["puerto"])
usuario = st.sidebar.text_input("Usuario", value=d["usuario"])
clave = st.sidebar.text_input("Contraseña", type="password", value=d["clave"])
nombre_bd = st.sidebar.text_input("Nombre de la BD / Ruta SQLite", value=d["nombre_bd"])

# ------------------------------
# Función para conectar y leer usuarios
# ------------------------------
def conectar_y_leer():
    global usuarios_unificados

    try:
        url = construir_url(tipo_bd)
        engine = create_engine(url)
        Base.metadata.create_all(engine)
        Session = sessionmaker(bind=engine)
        session = Session()
        usuarios = session.query(Usuario).all()
        session.close()

        usuarios_unificados = [{
            "id": u.id,
            "nombre": u.nombre,
            "email": u.email,
            "origen": tipo_bd
        } for u in usuarios]

        if usuarios_unificados:
            st.success(f"✅ Se encontraron {len(usuarios_unificados)} usuario(s) en la BD.")
        else:
            st.warning("⚠️ No se encontraron usuarios.")

    except Exception as e:
        st.error(f"❌ Error al conectar: {e}")

# ------------------------------
# Función para validar integridad
# ------------------------------
def validar_integridad():
    advertencias = validar_datos(usuarios_unificados)

    if not advertencias:
        st.success("✅ Todos los datos son válidos.")
    else:
        for adv in advertencias:
            st.warning(adv)

# ------------------------------
# Interfaz - Página principal
# ------------------------------
st.title("🧩 Plataforma de Integración de Bases de Datos Heterogéneas")

if st.button("🔌 Conectar y Leer"):
    conectar_y_leer()

if usuarios_unificados:
    st.subheader("👁️ Vista previa de usuarios")
    st.dataframe(usuarios_unificados)

    if st.button("🔎 Validar Integridad"):
        validar_integridad()

    # Prepara CSV para exportar como texto
    import io, csv
    buffer = io.StringIO()
    writer = csv.DictWriter(buffer, fieldnames=usuarios_unificados[0].keys())
    writer.writeheader()
    writer.writerows(usuarios_unificados)

    st.download_button(
        "💾 Exportar CSV",
        data=buffer.getvalue(),
        file_name=f"usuarios_{tipo_bd}.csv",
        mime="text/csv"
    )
