# modulos/sincronizacion.py

import streamlit as st
import pandas as pd
from utils.sync_logic import sync_universal
from sqlalchemy import inspect

def mostrar(df_integrado, motores, columnas_integradas):
    st.header("🔄 Sincronización Universal entre Bases de Datos")
    st.write("Esta sección permite sincronizar la tabla integrada con las bases de datos conectadas.")

    if df_integrado is None or df_integrado.empty:
        st.warning("⚠️ Primero debes integrar los datos antes de sincronizar.")
        return

    if not columnas_integradas:
        st.warning("⚠️ No se encontraron columnas válidas para sincronizar.")
        return

    # Convertimos a lista si es un diccionario
    if isinstance(columnas_integradas, dict):
        columnas_sincro = list(columnas_integradas.keys())
    else:
        columnas_sincro = columnas_integradas

    tabla_destino = st.text_input("Nombre de la tabla destino", "clientes")

    st.subheader("🔍 Previsualización de cambios por base de datos")

    diferencias_por_motor = {}
    for nombre_motor, engine in motores.items():
        try:
            df_destino = pd.read_sql_table(tabla_destino, engine)

            df_union = pd.concat([df_destino[columnas_sincro], df_integrado[columnas_sincro]], ignore_index=True).drop_duplicates()
            df_nuevos = df_union[~df_union.duplicated(subset=columnas_sincro, keep=False)]

            diferencias_por_motor[nombre_motor] = {
                "original": df_destino,
                "nuevos": df_nuevos
            }

            with st.expander(f"🛠 Cambios para {nombre_motor}"):
                st.write(f"📄 Registros actuales en {tabla_destino}: {len(df_destino)}")
                st.write(f"🆕 Registros nuevos a insertar: {len(df_nuevos)}")
                st.dataframe(df_nuevos.head(50))

        except Exception as e:
            st.error(f"❌ Error leyendo {tabla_destino} en {nombre_motor}: {e}")
            diferencias_por_motor[nombre_motor] = None

    if st.button("✅ Confirmar e Iniciar Sincronización"):
        with st.spinner("Sincronizando en segundo plano..."):
            resultados = sync_universal(df_integrado, motores, tabla_destino, columnas_sincro)

        st.subheader("📊 Resultados de la sincronización")
        for motor, resultado in resultados.items():
            st.markdown(f"- **{motor}** → {resultado}")

