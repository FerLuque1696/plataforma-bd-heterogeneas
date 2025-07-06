import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from sqlalchemy import inspect, create_engine
from urllib.parse import quote_plus

# ✔️ Nuevos valores reales
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
    },
    "mysql": {
        "host": "maglev.proxy.rlwy.net",
        "puerto": "24117",
        "usuario": "root",
        "clave": "UIgyVOyxdRLrEPwdZRKPRwTWhzrTyGmh",
        "nombre_bd": "railway"
    },
    "sqlserver": {
        "host": "DESKTOP-9EK5NEP",
        "puerto": "",
        "usuario": "",
        "clave": "",
        "nombre_bd": "tienda_sqlserver"
    }
}

# 🔧 Constructor universal de URL
def construir_url(motor, datos):
    if motor == "sqlite":
        return f"sqlite:///{datos['nombre_bd']}"
    elif motor == "postgres":
        return f"postgresql+psycopg2://{datos['usuario']}:{datos['clave']}@{datos['host']}:{datos['puerto']}/{datos['nombre_bd']}"
    elif motor == "mysql":
        return f"mysql+pymysql://{datos['usuario']}:{datos['clave']}@{datos['host']}:{datos['puerto']}/{datos['nombre_bd']}"
    elif motor == "sqlserver":
        return f"mssql+pyodbc://@{datos['host']}/{datos['nombre_bd']}?driver=ODBC+Driver+17+for+SQL+Server&trusted_connection=yes"
    else:
        raise ValueError("Motor no soportado")

@pytest.mark.parametrize("motor", list(valores_por_defecto.keys()))
def test_exploracion_tablas(motor):
    config = valores_por_defecto[motor]
    url = construir_url(motor, config)
    connect_args = {"check_same_thread": False} if motor == "sqlite" else {}

    try:
        engine = create_engine(url, connect_args=connect_args)
        inspector = inspect(engine)
        tablas = inspector.get_table_names()

        assert isinstance(tablas, list), f"No se obtuvo una lista de tablas para {motor}"
        for tabla in tablas:
            assert isinstance(tabla, str) and tabla.strip(), f"Nombre de tabla inválido: {tabla}"

    except Exception as e:
        pytest.fail(f"Exploración fallida en {motor}: {str(e)}")
