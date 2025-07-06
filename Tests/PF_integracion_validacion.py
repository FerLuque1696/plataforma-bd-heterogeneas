import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from sqlalchemy import create_engine, inspect

# Configuración directa sin necesidad de otros archivos
valores_por_defecto = {
    "sqlite": {
        "host": "localhost",
        "puerto": "",
        "usuario": "",
        "clave": "",
        "nombre_bd": "BDs_Prueba/SQLite/tienda_sqlite.db"
    },
    "postgres": {
        "host": "shinkansen.proxy.rlwy.net",
        "puerto": "12114",
        "usuario": "postgres",
        "clave": "fgCeonsIkhcHcZfHKBACqqyQMWsfJGVH",
        "nombre_bd": "railway"
    }
}

@pytest.mark.parametrize("motor_a, tabla_a, motor_b, tabla_b", [
    ("sqlite", "clientes", "postgres", "clientes")
])
def test_integracion_validacion_columnas(motor_a, tabla_a, motor_b, tabla_b):
    def_a = valores_por_defecto[motor_a]
    def_b = valores_por_defecto[motor_b]

    url_a = f"sqlite:///{def_a['nombre_bd']}"
    url_b = f"postgresql+psycopg2://{def_b['usuario']}:{def_b['clave']}@{def_b['host']}:{def_b['puerto']}/{def_b['nombre_bd']}"

    engine_a = create_engine(url_a)
    engine_b = create_engine(url_b)

    insp_a = inspect(engine_a)
    insp_b = inspect(engine_b)

    print(f"Tablas en {motor_a}: {insp_a.get_table_names()}")
    print(f"Tablas en {motor_b}: {insp_b.get_table_names()}")

    cols_a = {c["name"]: str(c["type"]).lower() for c in insp_a.get_columns(tabla_a)}
    cols_b = {c["name"]: str(c["type"]).lower() for c in insp_b.get_columns(tabla_b)}

    columnas_comunes = []
    for col_a, tipo_a in cols_a.items():
        for col_b, tipo_b in cols_b.items():
            if col_a.lower() == col_b.lower() and tipo_a[:5] == tipo_b[:5]:
                columnas_comunes.append((col_a, col_b))

    assert columnas_comunes, f"No se encontraron columnas compatibles entre {tabla_a} y {tabla_b}"
