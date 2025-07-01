import streamlit as st
from sqlalchemy import inspect
import pandas as pd
import graphviz


def mostrar_exploracion():
    st.title("🧩 Plataforma de Integración de Bases de Datos")

    motores = st.session_state.get("motores_conectados", {})
    tablas_motores = st.session_state.get("tablas_por_motor", {})

    if not motores:
        st.warning("Conéctate al menos a una base de datos desde el panel izquierdo.")
        return

    for motor_nombre, engine in motores.items():
        st.subheader(f"📊 Tablas en {motor_nombre.upper()}")
        tablas = tablas_motores.get(motor_nombre, [])

        if not tablas:
            st.info(f"No se encontraron tablas en {motor_nombre}")
            continue

        tabla_seleccionada = st.selectbox(
            f"Selecciona una tabla en {motor_nombre.lower()}:", tablas, key=motor_nombre
        )

        if tabla_seleccionada:
            inspector = inspect(engine)
            columnas = inspector.get_columns(tabla_seleccionada, schema="public" if motor_nombre == "postgres" else None)
            df_columnas = pd.DataFrame(columnas)[["name", "type"]].rename(columns={"name": "Columna", "type": "Tipo"})
            st.table(df_columnas)

            # Mostrar relaciones encontradas
            fks = inspector.get_foreign_keys(tabla_seleccionada, schema="public" if motor_nombre == "postgres" else None)
            if fks:
                st.markdown("### 🔗 Relaciones encontradas")
                relaciones = []
                for fk in fks:
                    for col in fk["constrained_columns"]:
                        relaciones.append({
                            "Desde": f"{tabla_seleccionada}.{col}",
                            "Hacia": f"{fk['referred_table']}.{fk['referred_columns'][0]}"
                        })
                st.dataframe(pd.DataFrame(relaciones))
            else:
                st.info("No se encontraron relaciones (llaves foráneas) para esta tabla.")

            # Mostrar diagrama ER para todas las tablas del motor
            generar_der(engine, motor_nombre)


def generar_der(motor, nombre_motor):
    inspector = inspect(motor)
    tablas = inspector.get_table_names(schema="public" if nombre_motor == "postgres" else None)

    dot = graphviz.Digraph("ER", format="png")
    dot.attr(rankdir="LR")

    for tabla in tablas:
        columnas = inspector.get_columns(tabla, schema="public" if nombre_motor == "postgres" else None)
        contenido = f"<<TABLE BORDER='0' CELLBORDER='1' CELLSPACING='0'>"
        contenido += f"<TR><TD BGCOLOR='#4472C4' COLSPAN='2'><FONT COLOR='white'><B>{tabla}</B></FONT></TD></TR>"

        for col in columnas:
            contenido += f"<TR><TD>{col['name']}</TD><TD>{str(col['type'])}</TD></TR>"

        contenido += "</TABLE>>"
        dot.node(tabla, contenido, shape="plaintext")

    for tabla in tablas:
        fks = inspector.get_foreign_keys(tabla, schema="public" if nombre_motor == "postgres" else None)
        for fk in fks:
            if fk["referred_table"]:
                dot.edge(tabla, fk["referred_table"], label=" ↳ " + ", ".join(fk["constrained_columns"]))

    st.markdown("### 🧠 Diagrama Entidad-Relación")
    st.graphviz_chart(dot)

