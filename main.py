# main.py — Plataforma base para integración y validación de usuarios

import streamlit as st
from db_utils import obtener_usuarios, exportar_csv_unificado
from validators import validar_datos

# ------------------------------
# Configuración de Streamlit
# ------------------------------
st.set_page_config(page_title="Integración Simple de Usuarios", layout="wide")
st.title("🧩 Plataforma Base de Integración")

# ------------------------------
# Selección de motores
# ------------------------------
st.sidebar.header("⚙️ Conexión")
motores_disponibles = ["sqlite", "postgres", "mysql", "sqlserver"]
motores_seleccionados = st.sidebar.multiselect("Selecciona motores a integrar", motores_disponibles)

usuarios_unificados = []

if st.sidebar.button("🔌 Conectar y Unificar"):
    for motor in motores_seleccionados:
        usuarios_unificados += obtener_usuarios(motor)

    if usuarios_unificados:
        st.success(f"✅ Se obtuvieron {len(usuarios_unificados)} usuarios unificados de {len(motores_seleccionados)} motores.")
    else:
        st.warning("⚠️ No se encontraron usuarios.")

# ------------------------------
# Mostrar y validar usuarios
# ------------------------------
if usuarios_unificados:
    st.subheader("👁️ Vista previa de usuarios integrados")
    st.dataframe(usuarios_unificados)

    if st.button("🔎 Validar Integridad"):
        advertencias = validar_datos(usuarios_unificados)
        if not advertencias:
            st.success("✅ Todos los datos son válidos.")
        else:
            for adv in advertencias:
                st.warning(adv)

    # Descargar como CSV
    import io, csv
    buffer = io.StringIO()
    writer = csv.DictWriter(buffer, fieldnames=usuarios_unificados[0].keys())
    writer.writeheader()
    writer.writerows(usuarios_unificados)

    st.download_button(
        "💾 Descargar CSV Unificado",
        data=buffer.getvalue(),
        file_name="usuarios_unificados.csv",
        mime="text/csv"
    )
else:
    st.info("ℹ️ Conecta y extrae usuarios para comenzar.")
