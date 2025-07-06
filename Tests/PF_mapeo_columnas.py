# Tests/PF_mapeo_columnas.py

import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from sqlalchemy import create_engine
from utils.integracion_utils import obtener_columnas_compatibles

# Configuración de motores reales
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

def construir_url(motor, conf):
    if motor == "sqlite":
        return f"sqlite:///{conf['nombre_bd']}"
    elif motor == "postgres":
        return f"postgresql+psycopg2://{conf['usuario']}:{conf['clave']}@{conf['host']}:{conf['puerto']}/{conf['nombre_bd']}"
    elif motor == "mysql":
        return f"mysql+pymysql://{conf['usuario']}:{conf['clave']}@{conf['host']}:{conf['puerto']}/{conf['nombre_bd']}"
    elif motor == "sqlserver":
        return f"mssql+pyodbc://@{conf['host']}/{conf['nombre_bd']}?driver=ODBC+Driver+17+for+SQL+Server&trusted_connection=yes"
    else:
        raise ValueError("Motor no soportado")

# Parámetros para probar combinaciones de motores y tablas
@pytest.mark.parametrize("motor1,tabla1,motor2,tabla2", [
    ("sqlite", "clientes", "sqlserver", "clientes"),
    ("postgres", "ventas", "mysql", "ventas"),
])
def test_columnas_compatibles(motor1, tabla1, motor2, tabla2):
    conf1 = valores_por_defecto[motor1]
    conf2 = valores_por_defecto[motor2]

    url1 = construir_url(motor1, conf1)
    url2 = construir_url(motor2, conf2)

    engine1 = create_engine(url1)
    engine2 = create_engine(url2)

    compatibles = obtener_columnas_compatibles(engine1, tabla1, engine2, tabla2)

    assert isinstance(compatibles, list), "El resultado no es una lista"
    assert all(len(tupla) == 2 for tupla in compatibles), "Cada item debe ser un par de columnas"
    assert len(compatibles) > 0, f"No se encontraron columnas compatibles entre {tabla1} y {tabla2}"
