# Tests/PF_sincronizacion_post_insercion.py

import pytest
import pandas as pd
from sqlalchemy import create_engine, inspect, text

valores_por_defecto = {
    "sqlite": {
        "nombre_bd": "BDs_Prueba/SQLite/tienda_sqlite.db"
    },
    "mysql": {
        "host": "maglev.proxy.rlwy.net",
        "puerto": "24117",
        "usuario": "root",
        "clave": "UIgyVOyxdRLrEPwdZRKPRwTWhzrTyGmh",
        "nombre_bd": "railway"
    }
}

@pytest.mark.parametrize("motor_origen, tabla_origen, motor_destino, tabla_destino", [
    ("sqlite", "clientes", "mysql", "clientes")
])
def test_sincronizacion_post_insercion(motor_origen, tabla_origen, motor_destino, tabla_destino):
    def origen_url(motor):
        db = valores_por_defecto[motor]["nombre_bd"]
        return f"sqlite:///{db}" if motor == "sqlite" else ""

    def destino_url(motor):
        datos = valores_por_defecto[motor]
        return f"mysql+pymysql://{datos['usuario']}:{datos['clave']}@{datos['host']}:{datos['puerto']}/{datos['nombre_bd']}"

    url_origen = origen_url(motor_origen)
    url_destino = destino_url(motor_destino)

    engine_origen = create_engine(url_origen)
    engine_destino = create_engine(url_destino)

    df_origen = pd.read_sql_table(tabla_origen, engine_origen)

    with engine_destino.begin() as conn:
        conn.execute(text("SET FOREIGN_KEY_CHECKS=0;"))  # Desactivar constraints
        conn.execute(text(f"DELETE FROM {tabla_destino}"))  # Limpiar tabla destino
        conn.execute(text("SET FOREIGN_KEY_CHECKS=1;"))  # Reactivar constraints

    # Insertar registros integrados
    df_origen.to_sql(tabla_destino, engine_destino, if_exists="append", index=False)

    # Verificar cantidad
    df_destino = pd.read_sql_table(tabla_destino, engine_destino)

    assert not df_destino.empty, "La tabla destino está vacía después de la sincronización."
    assert len(df_origen) == len(df_destino), "No se insertaron todos los registros correctamente."
