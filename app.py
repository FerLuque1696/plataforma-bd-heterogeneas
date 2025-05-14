import streamlit as st
from sqlalchemy import create_engine, inspect
import pandas as pd
import graphviz
from models import Base



# ------------------------------
# Estilo visual
# ------------------------------
st.set_page_config(page_title="Plataforma BDs", layout="wide")
st.markdown("""
    <style>
    body { background-color: #F1E5D8; }
    .main { background-color: #F1E5D8; }
    h1 { color: #6096AA; }
    h2 { color: #29738F; }
    .stButton > button { background-color: #29738F; color: white; }
    .stSelectbox label { color: #7F6F62; }
    .stDataFrame { background-color: #CEC2B8; }

    div[data-baseweb="select"] {
        margin-bottom: -10px;
        font-size: 13px !important;
    }
    .stSelectbox {
        padding-top: 0px !important;
        padding-bottom: 0px !important;
        margin-bottom: 4px !important;
    }
    </style>
""", unsafe_allow_html=True)

# ------------------------------
# Estado inicial
# ------------------------------
if "motores_conectados" not in st.session_state:
    st.session_state["motores_conectados"] = {}

if "tablas_por_motor" not in st.session_state:
    st.session_state["tablas_por_motor"] = {}

# ------------------------------
# Sidebar: conexión
# ------------------------------
st.sidebar.title("⚙️ Conexión")

tipo_bd = st.sidebar.selectbox("Tipo de Base de Datos", [
    "sqlite", "postgres", "mysql", "oracle", "sqlserver"
])

defaults = {
    "sqlite": {
        "host": "localhost",
        "puerto": "",
        "usuario": "",
        "clave": "",
        "nombre_bd": "BDs_Prueba/SQLite/bd_sqlite_demo.db"
    },
    "postgres": {
        "host": "localhost",
        "puerto": "5432",
        "usuario": "postgres",
        "clave": "123456",
        "nombre_bd": "bd_postgres_demo"
    },
    "mysql": {
        "host": "localhost",
        "puerto": "3306",
        "usuario": "root",
        "clave": "123456",
        "nombre_bd": "bd_mysql_demo"
    },
    "oracle": {
        "host": "localhost",
        "puerto": "1521",
        "usuario": "system",
        "clave": "123456",
        "nombre_bd": "XE"
    },
    "sqlserver": {
        "host": "DESKTOP-9EK5NEP",
        "puerto": "",
        "usuario": "",
        "clave": "",
        "nombre_bd": "bd_sqlserver_demo"
    }
}

d = defaults[tipo_bd]
host = st.sidebar.text_input("Host", value=d["host"])
puerto = st.sidebar.text_input("Puerto", value=d["puerto"])
usuario = st.sidebar.text_input("Usuario", value=d["usuario"])
clave = st.sidebar.text_input("Contraseña", type="password", value=d["clave"])
nombre_bd = st.sidebar.text_input(
    "Nombre de la BD / Ruta SQLite" if tipo_bd != "oracle" else "Service Name", value=d["nombre_bd"]
)

def construir_url(tipo, user, pwd, host, port, db):
    if tipo == "sqlite": return f"sqlite:///{db}"
    if tipo == "oracle": return f"oracle+oracledb://{user}:{pwd}@{host}:1521/?service_name={db}"
    if tipo == "sqlserver": return f"mssql+pyodbc://@{host}/{db}?driver=ODBC+Driver+17+for+SQL+Server&trusted_connection=yes"
    if tipo == "postgres": return f"postgresql+psycopg2://{user}:{pwd}@{host}:{port}/{db}"
    if tipo == "mysql": return f"mysql+pymysql://{user}:{pwd}@{host}:{port}/{db}"
    return None

if st.sidebar.button("🔌 Conectar"):
    try:
        url = construir_url(tipo_bd, usuario, clave, host, puerto, nombre_bd)
        engine = create_engine(url)
        inspector = inspect(engine)

        # Corrección: usar schema "public" en PostgreSQL, y UPPER en Oracle
        schema = "public" if tipo_bd == "postgres" else (usuario.upper() if tipo_bd == "oracle" else None)
        tablas = inspector.get_table_names(schema=schema)

        if not tablas:
            st.sidebar.warning("Conexión exitosa, pero no se encontraron tablas visibles en el esquema.")
        else:
            st.sidebar.success(f"Conectado a {tipo_bd.upper()} ({len(tablas)} tabla(s))")

        st.session_state["motores_conectados"][tipo_bd] = engine
        st.session_state["tablas_por_motor"][tipo_bd] = tablas

    except Exception as e:
        st.sidebar.error(f"❌ Error al conectar: {e}")


# ------------------------------
# Tabs principales
# ------------------------------
tab1, tab2 = st.tabs(["🔎 Exploración", "🔄 Integración"])

# ------------------------------
# TAB 1: Exploración
# ------------------------------
with tab1:
    st.title("🧩 Plataforma de Integración de Bases de Datos")

    for motor, engine in st.session_state["motores_conectados"].items():
        st.subheader(f"📋 Tablas en {motor.upper()}")
        inspector = inspect(engine)
        tablas = st.session_state["tablas_por_motor"].get(motor, [])

        if tablas:
            tabla_sel = st.selectbox(f"Selecciona una tabla en {motor}:", tablas, key=f"tabla_{motor}")
            columnas = inspector.get_columns(tabla_sel)
            st.table([{"Columna": c["name"], "Tipo": str(c["type"])} for c in columnas])

            # Detectar relaciones y generar diagrama ER
            relaciones = []
            for t in tablas:
                for fk in inspector.get_foreign_keys(t):
                    if fk["referred_table"]:
                        for local_col, remote_col in zip(fk["constrained_columns"], fk["referred_columns"]):
                            relaciones.append({
                                "Desde": f"{t}.{local_col}",
                                "Hacia": f"{fk['referred_table']}.{remote_col}"
                            })

            if relaciones:
                st.markdown("### 🔗 Relaciones encontradas")
                st.table(relaciones)

                dot = graphviz.Digraph("ER", format="png")
                dot.attr(rankdir="LR", size="8")

                for t in tablas:
                    cols = inspector.get_columns(t)
                    cab = f"<tr><td bgcolor='#6096AA'><b>{t}</b></td></tr>"
                    filas = "".join([f"<tr><td align='left'>{c['name']} : {c['type']}</td></tr>" for c in cols])
                    html = f"<<table border='0' cellborder='1' cellspacing='0'>{cab}{filas}</table>>"
                    dot.node(t, html)

                for rel in relaciones:
                    origen, destino = rel["Desde"].split(".")[0], rel["Hacia"].split(".")[0]
                    col = rel["Desde"].split(".")[1]
                    dot.edge(origen, destino, label=col, fontsize="10")

                st.markdown("### 🗺 Diagrama Entidad-Relación")
                st.graphviz_chart(dot)

            else:
                st.info("ℹ️ No se detectaron claves foráneas entre las tablas.")

# ------------------------------
# TAB 2: Integración
# ------------------------------
with tab2:
    st.title("🔄 Integración Inteligente de Tablas")

    if len(st.session_state["motores_conectados"]) < 2:
        st.warning("Conecta al menos dos motores para comenzar la integración.")
    else:
        motores = list(st.session_state["motores_conectados"].keys())

        col1, col2 = st.columns(2)
        with col1:
            motor_a = st.selectbox("🔹 Motor A", motores, key="motor_a")
            tabla_a = st.selectbox("Tabla A", st.session_state["tablas_por_motor"][motor_a], key="tabla_a")
        with col2:
            motor_b = st.selectbox("🔸 Motor B", [m for m in motores if m != motor_a], key="motor_b")
            tabla_b = st.selectbox("Tabla B", st.session_state["tablas_por_motor"][motor_b], key="tabla_b")

        if not tabla_a or not tabla_b:
            st.error("⚠️ Debes seleccionar dos tablas válidas para integrar.")
            st.stop()

        engine_a = st.session_state["motores_conectados"][motor_a]
        engine_b = st.session_state["motores_conectados"][motor_b]
        inspector_a = inspect(engine_a)
        inspector_b = inspect(engine_b)

        cols_a = [col["name"] for col in inspector_a.get_columns(tabla_a)]
        cols_b = [col["name"] for col in inspector_b.get_columns(tabla_b)]

        df_a = pd.read_sql_table(tabla_a, engine_a)
        df_b = pd.read_sql_table(tabla_b, engine_b)

        tipos_a = {col: str(df_a[col].dtype).upper() for col in df_a.columns}
        tipos_b = {col: str(df_b[col].dtype).upper() for col in df_b.columns}

        st.markdown("### 🔁 Configuración de Mapeo")

        mapeo = {}
        dot = graphviz.Digraph("Mapeo", format="png")
        dot.attr(rankdir="LR", size="5,3", fontsize="10")

        for col in cols_a:
            dot.node(f"A_{col}", f"A: {col}", shape="box", style="filled", fillcolor="#D6EAF8")
        for col in cols_b:
            dot.node(f"B_{col}", f"B: {col}", shape="box", style="filled", fillcolor="#F9E79F")

        col_map1, col_map2 = st.columns(2)
        for i, col_a in enumerate(cols_a):
            target_col = col_map1 if i % 2 == 0 else col_map2
            with target_col:
                col_b = st.selectbox(f"🧩 '{col_a}' ↔", ["(ignorar)"] + cols_b, key=f"map_{col_a}")
                if col_b != "(ignorar)":
                    mapeo[col_a] = col_b
                    dot.edge(f"A_{col_a}", f"B_{col_b}", label="→", color="black")

        st.markdown("### 🖇 Diagrama de Mapeo Visual")
        st.graphviz_chart(dot, use_container_width=True)

        if mapeo:
            st.markdown("### 🧮 Resumen de columnas mapeadas")
            filas = []
            for col_a in cols_a:
                col_b = mapeo.get(col_a)
                tipo_a = tipos_a.get(col_a, "-")
                tipo_b = tipos_b.get(col_b, "-") if col_b else "-"
                estado = "✔ Mapeado" if col_b else "✖ No mapeado"
                if col_b and tipo_a != tipo_b:
                    estado = "⚠ Tipos distintos"
                filas.append({
                    "Columna A": col_a,
                    "Columna B": col_b or "(ninguna)",
                    "Tipo A": tipo_a,
                    "Tipo B": tipo_b,
                    "Estado": estado
                })
            st.dataframe(pd.DataFrame(filas), use_container_width=True)

            df_b_ren = df_b.rename(columns={v: k for k, v in mapeo.items()})
            df_a_f = df_a[list(mapeo.keys())]
            df_b_f = df_b_ren[list(mapeo.keys())]

            df_merged = pd.concat([df_a_f, df_b_f], ignore_index=True).drop_duplicates()
            st.success(f"✅ {df_merged.shape[0]} registros unificados.")
            st.dataframe(df_merged, use_container_width=True)
        else:
            st.info("Mapea al menos una columna para visualizar la integración.")
