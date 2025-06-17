# app.py (documentado completamente para principiantes y siguiendo buenas prácticas)

# ------------------------------
# Importaciones necesarias
# ------------------------------
import streamlit as st
from sqlalchemy import create_engine, inspect
import pandas as pd
import graphviz
from models import Base
from validators import validar_generico
import io

# ------------------------------
# Configuración inicial de la página
# ------------------------------
st.set_page_config(page_title="Plataforma BDs", layout="wide")

# ------------------------------
# Estilos visuales personalizados
# ------------------------------
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
# Estado inicial (sesión)
# ------------------------------
if "motores_conectados" not in st.session_state:
    st.session_state["motores_conectados"] = {}

if "tablas_por_motor" not in st.session_state:
    st.session_state["tablas_por_motor"] = {}

# ------------------------------
# Sidebar: Conexión a base de datos
# ------------------------------
st.sidebar.title("⚙️ Conexión")

tipo_bd = st.sidebar.selectbox("Tipo de Base de Datos", ["sqlite", "postgres", "mysql", "sqlserver"])

# Valores por defecto por motor
valores_por_defecto = {
    "sqlite": {"host": "localhost", "puerto": "", "usuario": "", "clave": "", "nombre_bd": "BDs_Prueba/SQLite/bd_sqlite_demo.db"},
    "postgres": {"host": "localhost", "puerto": "5432", "usuario": "postgres", "clave": "123456", "nombre_bd": "bd_postgres_demo"},
    "mysql": {"host": "localhost", "puerto": "3306", "usuario": "root", "clave": "123456", "nombre_bd": "bd_mysql_demo"},
    "sqlserver": {"host": "DESKTOP-9EK5NEP", "puerto": "", "usuario": "", "clave": "", "nombre_bd": "bd_sqlserver_demo"}
}

valores = valores_por_defecto[tipo_bd]
host = st.sidebar.text_input("Host", value=valores["host"])
puerto = st.sidebar.text_input("Puerto", value=valores["puerto"])
usuario = st.sidebar.text_input("Usuario", value=valores["usuario"])
clave = st.sidebar.text_input("Contraseña", type="password", value=valores["clave"])
nombre_bd = st.sidebar.text_input("Nombre de la BD / Ruta SQLite", value=valores["nombre_bd"])

# Construcción de URL de conexión

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

# Botón para conectar
if st.sidebar.button("🔌 Conectar"):
    try:
        url_conexion = construir_url(tipo_bd, usuario, clave, host, puerto, nombre_bd)
        motor = create_engine(url_conexion)
        inspector = inspect(motor)
        esquema = "public" if tipo_bd == "postgres" else None
        tablas = inspector.get_table_names(schema=esquema)

        if not tablas:
            st.sidebar.warning("Conexión exitosa, pero no se encontraron tablas visibles en el esquema.")
        else:
            st.sidebar.success(f"Conectado a {tipo_bd.upper()} ({len(tablas)} tabla(s))")

        st.session_state["motores_conectados"][tipo_bd] = motor
        st.session_state["tablas_por_motor"][tipo_bd] = tablas

    except Exception as error:
        st.sidebar.error(f"❌ Error al conectar: {error}")

# ------------------------------
# TAB 1: Exploración de tablas conectadas
# ------------------------------
tab_exploracion, tab_integracion, tab_carga = st.tabs(["🔎 Exploración", "🔄 Integración", "⚙️ Cargar en BD"])

with tab_exploracion:
    st.title("🧩 Plataforma de Integración de Bases de Datos")

    for nombre_motor, motor_conectado in st.session_state["motores_conectados"].items():
        st.subheader(f"📋 Tablas disponibles en {nombre_motor.upper()}")
        inspector = inspect(motor_conectado)
        lista_tablas = st.session_state["tablas_por_motor"].get(nombre_motor, [])

        if lista_tablas:
            tabla_seleccionada = st.selectbox(f"Selecciona una tabla en {nombre_motor}:", lista_tablas, key=f"tabla_{nombre_motor}")
            columnas = inspector.get_columns(tabla_seleccionada)
            st.table([{"Columna": col["name"], "Tipo": str(col["type"])} for col in columnas])

            # Analizar claves foráneas y relaciones
            relaciones = []
            for tabla in lista_tablas:
                for fk in inspector.get_foreign_keys(tabla):
                    if fk["referred_table"]:
                        for col_local, col_remota in zip(fk["constrained_columns"], fk["referred_columns"]):
                            relaciones.append({
                                "Desde": f"{tabla}.{col_local}",
                                "Hacia": f"{fk['referred_table']}.{col_remota}"
                            })

            # Mostrar relaciones si las hay
            if relaciones:
                st.markdown("### 🔗 Relaciones encontradas entre tablas")
                st.table(relaciones)

                dot = graphviz.Digraph("ER", format="png")
                dot.attr(rankdir="LR", size="8")

                for tabla in lista_tablas:
                    columnas_tabla = inspector.get_columns(tabla)
                    cabecera = f"<tr><td bgcolor='#6096AA'><b>{tabla}</b></td></tr>"
                    filas = "".join([f"<tr><td align='left'>{col['name']} : {col['type']}</td></tr>" for col in columnas_tabla])
                    html = f"<<table border='0' cellborder='1' cellspacing='0'>{cabecera}{filas}</table>>"
                    dot.node(tabla, html)

                for relacion in relaciones:
                    tabla_origen, tabla_destino = relacion["Desde"].split(".")[0], relacion["Hacia"].split(".")[0]
                    columna_origen = relacion["Desde"].split(".")[1]
                    dot.edge(tabla_origen, tabla_destino, label=columna_origen, fontsize="10")

                st.markdown("### 🗺 Diagrama Entidad-Relación (ER)")
                st.graphviz_chart(dot)
            else:
                st.info("ℹ️ No se detectaron claves foráneas entre las tablas conectadas.")

# ------------------------------
# TAB 2: Integración de Datos
# ------------------------------
with tab_integracion:
    st.title("🔄 Integración Inteligente de Tablas")

    # Verificar que al menos 2 motores estén conectados para permitir integración
    if len(st.session_state["motores_conectados"]) < 2:
        st.warning("Conecta al menos dos motores para comenzar la integración.")
    else:
        motores = list(st.session_state["motores_conectados"].keys())

        # Selección de motores y tablas de origen A y B
        col1, col2 = st.columns(2)
        with col1:
            motor_a = st.selectbox("🔹 Motor A", motores, key="motor_a")
            tabla_a = st.selectbox("Tabla A", st.session_state["tablas_por_motor"][motor_a], key="tabla_a")
        with col2:
            motor_b = st.selectbox("🔸 Motor B", [m for m in motores if m != motor_a], key="motor_b")
            tabla_b = st.selectbox("Tabla B", st.session_state["tablas_por_motor"][motor_b], key="tabla_b")

        # Validación de selección
        if not tabla_a or not tabla_b:
            st.error("⚠️ Debes seleccionar dos tablas válidas para integrar.")
            st.stop()

        # Obtener motores e inspectores
        engine_a = st.session_state["motores_conectados"][motor_a]
        engine_b = st.session_state["motores_conectados"][motor_b]
        inspector_a = inspect(engine_a)
        inspector_b = inspect(engine_b)

        # Obtener nombres de columnas
        cols_a = [col["name"] for col in inspector_a.get_columns(tabla_a)]
        cols_b = [col["name"] for col in inspector_b.get_columns(tabla_b)]

        # Cargar los datos en DataFrames
        df_a = pd.read_sql_table(tabla_a, engine_a)
        df_b = pd.read_sql_table(tabla_b, engine_b)

        # Tipos de columnas para comparación
        tipos_a = {col: str(df_a[col].dtype).upper() for col in df_a.columns}
        tipos_b = {col: str(df_b[col].dtype).upper() for col in df_b.columns}

        st.markdown("### 🔁 Configuración de Mapeo")

        mapeo = {}  # Diccionario para almacenar el mapeo de columnas

        # Crear grafo para visualización del mapeo
        dot = graphviz.Digraph("Mapeo", format="png")
        dot.attr(rankdir="LR", size="5,3", fontsize="10")

        # Nodos para columnas de tabla A
        for col in cols_a:
            dot.node(f"A_{col}", f"A: {col}", shape="box", style="filled", fillcolor="#D6EAF8")

        # Nodos para columnas de tabla B
        for col in cols_b:
            dot.node(f"B_{col}", f"B: {col}", shape="box", style="filled", fillcolor="#F9E79F")

        # Interfaz para que el usuario seleccione el mapeo entre columnas
        col_map1, col_map2 = st.columns(2)
        for i, col_a in enumerate(cols_a):
            target_col = col_map1 if i % 2 == 0 else col_map2
            with target_col:
                col_b = st.selectbox(f"🧩 '{col_a}' ↔", ["(ignorar)"] + cols_b, key=f"map_{col_a}")
                if col_b != "(ignorar)":
                    mapeo[col_a] = col_b
                    dot.edge(f"A_{col_a}", f"B_{col_b}", label="→", color="black")

        # Mostrar el diagrama de mapeo visual
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

            # Renombrar columnas de df_b al nombre de df_a para unificación
            df_b_renombrado = df_b.rename(columns={v: k for k, v in mapeo.items()})
            df_a_filtrado = df_a[list(mapeo.keys())]
            df_b_filtrado = df_b_renombrado[list(mapeo.keys())]

            # Unir los dos DataFrames sin duplicados
            df_merged = pd.concat([df_a_filtrado, df_b_filtrado], ignore_index=True).drop_duplicates()
            st.success(f"✅ {df_merged.shape[0]} registros unificados.")
            st.dataframe(df_merged, use_container_width=True)

            # Validar los datos integrados con función genérica
            st.markdown("### ✅ Validación de Integridad de Datos Integrados")
            advertencias = validar_generico(df_merged, engine_b, tabla_b)

            if not advertencias:
                st.success("✔ Todos los registros unificados son válidos.")
            else:
                for advertencia in advertencias:
                    st.warning(advertencia)

            # Opción para descargar los datos unificados
            st.markdown("### 📥 Descargar Resultado Integrado")
            buffer_csv = io.StringIO()
            df_merged.to_csv(buffer_csv, index=False)
            st.download_button(
                label="💾 Descargar CSV",
                data=buffer_csv.getvalue(),
                file_name="datos_unificados.csv",
                mime="text/csv"
            )
        else:
            st.info("Mapea al menos una columna para visualizar la integración.")
            
# ------------------------------
# TAB 3: Carga de Datos en Base de Datos
# ------------------------------
with tab_carga:
    st.title("⚙️ Carga Directa en Base de Datos")

    # Validar si ya se realizó una integración
    if "df_merged" not in locals() or "tabla_b" not in locals() or "motor_b" not in locals():
        st.info("ℹ️ Primero realiza una integración válida para habilitar esta opción.")
        st.stop()

    if not st.session_state["motores_conectados"]:
        st.warning("⚠️ No hay motores conectados.")
        st.stop()

    motores = [motor_b] if motor_b in st.session_state["motores_conectados"] else []

    if not motores:
        st.error("❌ No se encontró el motor de destino utilizado en la integración previa.")
        st.stop()

    motor_destino = st.selectbox("🛢 Motor de destino (utilizado en integración)", motores, key="crud_motor")

    engine = st.session_state["motores_conectados"][motor_destino]
    inspector = inspect(engine)
    tablas_destino = st.session_state["tablas_por_motor"].get(motor_destino, [])

    if tabla_b not in tablas_destino:
        st.error(f"❌ La tabla '{tabla_b}' no se encuentra en el motor de destino.")
        st.stop()

    tabla_destino = st.selectbox("📥 Tabla destino (de la integración)", [tabla_b], key="crud_tabla")

    columnas_destino = [col["name"] for col in inspector.get_columns(tabla_destino)]

    st.markdown("### 👁️ Vista previa de datos a insertar")
    st.dataframe(df_merged, use_container_width=True)

    st.markdown("### ⚠️ Compatibilidad de columnas")
    columnas_compatibles = set(df_merged.columns).issubset(set(columnas_destino))

    if columnas_compatibles:
        st.success("✔ Las columnas del DataFrame son compatibles con la tabla destino.")
    else:
        st.error("❌ Las columnas del DataFrame NO coinciden con las de la tabla destino.")
        columnas_faltantes = list(set(df_merged.columns) - set(columnas_destino))
        st.write("🧾 Columnas faltantes en la tabla destino:", columnas_faltantes)
        st.stop()

    if st.button("🚀 Insertar en la base de datos (autogenerar PKs)"):
        try:
            columnas_pk = inspector.get_pk_constraint(tabla_destino).get("constrained_columns", [])

            # Excluir columnas PK y columnas NOT NULL sin default
            columnas_notnull = [col["name"] for col in inspector.get_columns(tabla_destino) if not col.get("nullable", True) and not col.get("default")]
            columnas_excluir = list(set(columnas_pk).intersection(df_merged.columns))

            df_insertar = df_merged.drop(columns=columnas_excluir, errors="ignore")
            df_insertar = df_insertar.drop_duplicates()

            # Verificar que ninguna columna NOT NULL quede como nula
            nulas_invalidas = df_insertar[columnas_notnull].isnull().any(axis=1)
            if nulas_invalidas.any():
                st.error("❌ No se pueden insertar registros con valores nulos en columnas obligatorias:")
                st.dataframe(df_insertar[nulas_invalidas], use_container_width=True)
                st.stop()

            df_insertar.to_sql(tabla_destino, engine, if_exists="append", index=False)

            st.success(f"✅ Se insertaron {len(df_insertar)} registro(s) correctamente en '{tabla_destino}' de {motor_destino.upper()} (PKs generadas automáticamente si aplica)")
        except Exception as error:
            st.error(f"❌ Error al insertar los datos: {error}")