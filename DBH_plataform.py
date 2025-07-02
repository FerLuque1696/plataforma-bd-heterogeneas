import streamlit as st
import pandas as pd
import graphviz
from sqlalchemy import inspect, create_engine

from modulos import exploracion, integracion, sincronizacion  # Eliminamos carga

st.set_page_config(page_title="Plataforma BDs", layout="wide")
st.markdown("""<style>
    body { background-color: #F1E5D8; }
    .main { background-color: #F1E5D8; }
    h1 { color: #6096AA; }
    h2 { color: #29738F; }
    .stButton > button { background-color: #29738F; color: white; }
</style>""", unsafe_allow_html=True)

# Estado de sesión
if "motores_conectados" not in st.session_state:
    st.session_state["motores_conectados"] = {}
if "tablas_por_motor" not in st.session_state:
    st.session_state["tablas_por_motor"] = {}

# --- SIDEBAR DE CONEXIÓN ---
st.sidebar.title("⚙️ Conexión")

tipo_bd = st.sidebar.selectbox("Tipo de Base de Datos", ["sqlite", "postgres", "mysql", "sqlserver"])
valores_por_defecto = {
    "sqlite": {"host": "localhost", "puerto": "", "usuario": "", "clave": "", "nombre_bd": "BDs_Prueba/SQLite/tienda_sqlite.db"},
    "postgres": {"host": "localhost", "puerto": "5432", "usuario": "postgres", "clave": "123456", "nombre_bd": "tienda_postgres"},
    "mysql": {"host": "localhost", "puerto": "3306", "usuario": "root", "clave": "123456", "nombre_bd": "tienda_mysql"},
    "sqlserver": {"host": "DESKTOP-9EK5NEP", "puerto": "", "usuario": "", "clave": "", "nombre_bd": "tienda_sqlserver"}
}
v = valores_por_defecto[tipo_bd]

host = st.sidebar.text_input("Host", value=v["host"])
puerto = st.sidebar.text_input("Puerto", value=v["puerto"])
usuario = st.sidebar.text_input("Usuario", value=v["usuario"])
clave = st.sidebar.text_input("Contraseña", type="password", value=v["clave"])
nombre_bd = st.sidebar.text_input("Nombre de la BD / Ruta SQLite", value=v["nombre_bd"])

def construir_url(tipo, user, pwd, host, port, db):
    if tipo == "sqlite":
        return f"sqlite:///{db}"
    if tipo == "sqlserver":
        return f"mssql+pyodbc://@{host}/{db}?driver=ODBC+Driver+17+for+SQL+Server&trusted_connection=yes"
    if tipo == "postgres":
        return f"postgresql+psycopg2://{user}:{pwd}@{host}:{port}/{db}"
    if tipo == "mysql":
        return f"mysql+pymysql://{user}:{pwd}@{host}:{port}/{db}"
    return None

if st.sidebar.button("🔌 Conectar"):
    try:
        url = construir_url(tipo_bd, usuario, clave, host, puerto, nombre_bd)
        motor = st.session_state.motores_conectados.get(tipo_bd) or None
        motor = motor or create_engine(url)
        inspector = inspect(motor)
        tablas = inspector.get_table_names(schema="public" if tipo_bd == "postgres" else None)
        st.session_state["motores_conectados"][tipo_bd] = motor
        st.session_state["tablas_por_motor"][tipo_bd] = tablas
        st.sidebar.success(f"Conectado a {tipo_bd.upper()} ({len(tablas)} tabla(s))")
    except Exception as e:
        st.sidebar.error(f"❌ Error: {e}")

# --- TABS PRINCIPALES ---
tab1, tab2, tab3 = st.tabs(["🔎 Exploración", "🔄 Integración", "🔃 Sincronización"])

with tab1:
    exploracion.mostrar_exploracion()

with tab2:
    integracion.mostrar_integracion()

with tab3:
    sincronizacion.mostrar(
        st.session_state.get("tabla_integrada"),
        st.session_state.get("motores_conectados"),
        st.session_state.get("columnas_mapeadas")
    )