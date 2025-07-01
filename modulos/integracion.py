import streamlit as st
import pandas as pd
import graphviz
from sqlalchemy import inspect


def mostrar_integracion():
    st.title("🔄 Integración Inteligente de Tablas")

    motores = list(st.session_state.get("motores_conectados", {}).keys())
    if len(motores) < 2:
        st.warning("Debes conectar al menos dos motores para realizar la integración.")
        return

    col1, col2 = st.columns(2)
    with col1:
        motor_a = st.selectbox("🔷 Motor A", motores, key="motor_a")
        tablas_a = obtener_tablas(motor_a)
        tabla_a = st.selectbox("Tabla A", tablas_a, key="tabla_a")
    with col2:
        motores_b = [m for m in motores if m != motor_a]
        motor_b = st.selectbox("🟠 Motor B", motores_b, key="motor_b")
        tablas_b = obtener_tablas(motor_b)
        tabla_b = st.selectbox("Tabla B", tablas_b, key="tabla_b")

    columnas_a = obtener_columnas(motor_a, tabla_a)
    columnas_b = obtener_columnas(motor_b, tabla_b)

    st.subheader("🧩 Configuración de Mapeo")
    mapeo = {}
    for i in range(0, len(columnas_a), 3):
        cols = st.columns(3)
        for j in range(3):
            if i + j < len(columnas_a):
                col = columnas_a[i + j]
                opciones = ["(ignorar)"] + columnas_b
                seleccion = cols[j].selectbox(f"🔹 {col} →", opciones, key=f"map_{col}")
                if seleccion != "(ignorar)":
                    mapeo[col] = seleccion

    st.subheader("🧬 Diagrama de Mapeo Visual")
    if mapeo:
        dot = graphviz.Digraph()
        dot.attr(rankdir='LR')

        with dot.subgraph(name='clusterA') as c:
            c.attr(label=tabla_a, style='filled', color='lightgrey')
            for col in mapeo.keys():
                c.node(f"A_{col}", col)

        with dot.subgraph(name='clusterB') as c:
            c.attr(label=tabla_b, style='filled', color='lightblue')
            for col in mapeo.values():
                c.node(f"B_{col}", col)

        for col_a, col_b in mapeo.items():
            dot.edge(f"A_{col_a}", f"B_{col_b}")

        st.graphviz_chart(dot)

        st.subheader("✅ Validación de Integridad de Datos")
        try:
            df_a = pd.read_sql_table(tabla_a, st.session_state.motores_conectados[motor_a])
            df_b = pd.read_sql_table(tabla_b, st.session_state.motores_conectados[motor_b])
            columnas_a_set = set(df_a.columns)
            columnas_b_set = set(df_b.columns)

            if not all(mapeo[k] in columnas_b_set for k in mapeo):
                st.warning("Hay columnas seleccionadas que no existen en la tabla destino. Revisa el mapeo.")
            else:
                columnas_info_a = {col["name"]: str(col["type"]).lower() for col in inspect(st.session_state.motores_conectados[motor_a]).get_columns(tabla_a)}
                columnas_info_b = {col["name"]: str(col["type"]).lower() for col in inspect(st.session_state.motores_conectados[motor_b]).get_columns(tabla_b)}
                tipos_incompatibles = []
                for col_a, col_b in mapeo.items():
                    tipo_a = columnas_info_a[col_a]
                    tipo_b = columnas_info_b[col_b]
                    if tipo_a != tipo_b:
                        tipos_incompatibles.append((col_a, tipo_a, col_b, tipo_b))

                if tipos_incompatibles:
                    st.warning("Se encontraron columnas mapeadas con tipos incompatibles:")
                    for col_a, tipo_a, col_b, tipo_b in tipos_incompatibles:
                        st.text(f"{col_a} ({tipo_a}) ≠ {col_b} ({tipo_b})")
                else:
                    cols_a = list(mapeo.keys())
                    cols_b = [mapeo[c] for c in cols_a]
                    if df_a[cols_a].isnull().any().any() or df_b[cols_b].isnull().any().any():
                        st.warning("Se encontraron valores nulos en las columnas seleccionadas. Revisa la limpieza de datos.")
                    else:
                        st.success("Las columnas seleccionadas son válidas, con tipos compatibles y sin valores nulos. Los datos están listos para integrarse.")
        except Exception as e:
            st.error(f"Error durante la validación de integridad: {e}")

        st.subheader("📋 Vista Previa de Integración")
        try:
            df_renamed_b = df_b.rename(columns={mapeo[a]: a for a in mapeo})
            df_merge = pd.concat([df_a[mapeo.keys()], df_renamed_b[mapeo.keys()]], ignore_index=True)
            st.dataframe(df_merge.head(100))

            st.session_state["tabla_integrada"] = df_merge
            st.session_state["columnas_mapeadas"] = mapeo
            st.session_state["origenes_integracion"] = {
                "motor_a": motor_a,
                "tabla_a": tabla_a,
                "motor_b": motor_b,
                "tabla_b": tabla_b
            }
        except Exception as e:
            st.error(f"Error al integrar: {e}")
    else:
        st.info("Selecciona al menos un par de columnas para generar el grafo.")

def obtener_tablas(motor):
    engine = st.session_state.motores_conectados[motor]
    inspector = inspect(engine)
    return inspector.get_table_names()

def obtener_columnas(motor, tabla):
    engine = st.session_state.motores_conectados[motor]
    inspector = inspect(engine)
    columnas = inspector.get_columns(tabla)
    return [col["name"] for col in columnas]
