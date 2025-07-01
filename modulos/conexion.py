# pages/conexion.py

import streamlit as st
from sqlalchemy import create_engine, inspect

def mostrar_conexion():
    st.sidebar.title("⚙️ Conexión")

    # Tipos de motor disponibles
    tipo_bd = st.sidebar.selectbox("Tipo de Base de Datos", ["sqlite", "postgres", "mysql", "sqlserver"])

    # Valores por defecto por motor
    valores_por_defecto = {
        "sqlite": {
            "host": "localhost", "puerto": "", "usuario": "", "clave": "",
            "nombre_bd": "BDs_Prueba/SQLite/bd_sqlite_demo.db"
        },
        "postgres": {
            "host": "localhost", "puerto": "5432", "usuario": "postgres", "clave": "123456",
            "nombre_bd": "bd_postgres_demo"
        },
        "mysql": {
            "host": "localhost", "puerto": "3306", "usuario": "root", "clave": "123456",
            "nombre_bd": "bd_mysql_demo"
        },
        "sqlserver": {
            "host": "DESKTOP-9EK5NEP", "puerto": "", "usuario": "", "clave": "",
            "nombre_bd": "bd_sqlserver_demo"
        }
    }

    v = valores_por_defecto[tipo_bd]

    # Inputs con autocompletado
    host = st.sidebar.text_input("Host", value=v["host"])
    puerto = st.sidebar.text_input("Puerto", value=v["puerto"])
    usuario = st.sidebar.text_input("Usuario", value=v["usuario"])
    clave = st.sidebar.text_input("Contraseña", type="password", value=v["clave"])
    nombre_bd = st.sidebar.text_input("Nombre de la BD / Ruta SQLite", value=v["nombre_bd"])

    def construir_url(tipo, user, pwd, host, port, db):
        if tipo == "sqlite":
            return f"sqlite:///{db}"
        elif tipo == "sqlserver":
            return f"mssql+pyodbc://@{host}/{db}?driver=ODBC+Driver+17+for+SQL+Server&trusted_connection=yes"
        elif tipo == "postgres":
            return f"postgresql+psycopg2://{user}:{pwd}@{host}:{port}/{db}"
        elif tipo == "mysql":
            return f"mysql+pymysql://{user}:{pwd}@{host}:{port}/{db}"
        else:
            return None

    # Botón conectar
    if st.sidebar.button("🔌 Conectar"):
        try:
            url_conexion = construir_url(tipo_bd, usuario, clave, host, puerto, nombre_bd)
            engine = create_engine(url_conexion)
            inspector = inspect(engine)
            tablas = inspector.get_table_names()

            if "motores_conectados" not in st.session_state:
                st.session_state.motores_conectados = {}
            if "tablas_por_motor" not in st.session_state:
                st.session_state.tablas_por_motor = {}

            st.session_state.motores_conectados[tipo_bd] = engine
            st.session_state.tablas_por_motor[tipo_bd] = tablas

            if not tablas:
                st.sidebar.warning("Conexión exitosa, pero no se encontraron tablas visibles.")
            else:
                st.sidebar.success(f"Conectado a {tipo_bd.upper()} ({len(tablas)} tabla(s))")

        except Exception as e:
            st.sidebar.error(f"❌ Error al conectar: {e}")
