import streamlit as st
import pandas as pd
from sqlalchemy import inspect

def mostrar(df_integrado, motores, columnas_integradas):
    st.header("🔄 Sincronización Universal entre Bases de Datos")

    if not st.session_state.get("sync_preparado"):
        st.info("⚠️ Primero debes integrar los datos y presionar el botón 'Enviar a sincronización'.")
        return

    if df_integrado is None or df_integrado.empty:
        st.warning("⚠️ No hay datos integrados disponibles.")
        return

    if not columnas_integradas:
        st.warning("⚠️ No se definieron columnas válidas para sincronización.")
        return

    info = st.session_state.get("tablas_para_sincronizar", {})
    tabla_a = info.get("tabla_a", "¿?")
    tabla_b = info.get("tabla_b", "¿?")
    motor_a = info.get("motor_a", "¿?")
    motor_b = info.get("motor_b", "¿?")

    st.markdown(f"""
    🔹 **Origen A:** `{tabla_a}` en `{motor_a}`  
    🔸 **Origen B:** `{tabla_b}` en `{motor_b}`
    """)

    st.subheader("🔍 Vista previa de registros a sincronizar")
    motores_usados = {motor_a: motores[motor_a], motor_b: motores[motor_b]}
    diferencias_por_motor = {}

    col1, col2 = st.columns(2)

    for idx, (nombre_motor, engine) in enumerate(motores_usados.items()):
        try:
            tabla_origen = tabla_a if nombre_motor == motor_a else tabla_b
            insp = inspect(engine)
            df_destino = pd.read_sql_table(tabla_origen, engine)

            # Obtener columnas únicas además de PK
            unique_cols = set()
            pk = insp.get_pk_constraint(tabla_origen).get("constrained_columns", [])
            for constraint in insp.get_unique_constraints(tabla_origen):
                unique_cols.update(constraint.get("column_names", []))
            columnas_criticas = list(set(columnas_integradas).union(unique_cols))

            df_union = pd.concat([df_destino, df_integrado], ignore_index=True).drop_duplicates()
            df_nuevos = df_union[~df_union.duplicated(subset=columnas_criticas, keep=False)]

            diferencias_por_motor[nombre_motor] = {
                "original": df_destino,
                "nuevos": df_nuevos,
                "tabla": tabla_origen,
                "engine": engine,
                "pk": pk,
                "unique": list(unique_cols)
            }

            with (col1 if idx == 0 else col2):
                st.markdown(f"### 📊 {nombre_motor}")
                st.markdown(f"**Tabla actual ({tabla_origen})**")
                st.dataframe(df_destino.head(30), use_container_width=True)
                st.markdown("**➕ Registros nuevos que se añadirán:**")
                st.dataframe(df_nuevos.head(30), use_container_width=True)

        except Exception as e:
            st.error(f"❌ Error al leer tabla desde {nombre_motor}: {e}")
            diferencias_por_motor[nombre_motor] = None

    if st.button("✅ Confirmar e Iniciar Sincronización"):
        with st.spinner("Sincronizando datos en ambos motores..."):
            resultados = {}

            for motor, info in diferencias_por_motor.items():
                if info and info["nuevos"] is not None:
                    try:
                        df_nuevos = info["nuevos"].copy()
                        engine = info["engine"]
                        tabla = info["tabla"]
                        pk = info["pk"]
                        columnas_unicas = info["unique"]

                        # Excluir columnas protegidas
                        columnas = inspect(engine).get_columns(tabla)
                        columnas_excluir = set()
                        for col in columnas:
                            if col.get("autoincrement") or col["name"] in pk:
                                columnas_excluir.add(col["name"])

                        # También excluir columnas únicas para no forzar valores
                        columnas_excluir.update(columnas_unicas)

                        df_a_insertar = df_nuevos.drop(columns=columnas_excluir, errors="ignore")

                        if not df_a_insertar.empty:
                            df_a_insertar.to_sql(tabla, con=engine, if_exists='append', index=False)
                            resultados[motor] = f"✅ Insertados {len(df_a_insertar)} registros nuevos"
                        else:
                            resultados[motor] = "🟦 Sin cambios (ya existen o sin nuevos registros)"

                    except Exception as e:
                        resultados[motor] = f"❌ Error al insertar: {str(e)}"

        st.subheader("📊 Resultados de la sincronización")
        for motor, resultado in resultados.items():
            color = "🟢" if resultado.startswith("✅") else "🔴"
            st.markdown(f"- **{motor}** → {color} {resultado}")
