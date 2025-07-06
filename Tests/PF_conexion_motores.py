# tests/PF_conexion_motores.py
import pytest
from sqlalchemy import create_engine, inspect
from sqlalchemy.exc import OperationalError
from urllib.parse import quote_plus

# Diccionario con las conexiones reales
valores_por_defecto = {
    "sqlite": {
        "host": "",
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

motores = ["sqlite", "postgres", "mysql", "sqlserver"]

def construir_url(tipo, user, pwd, host, port, db):
    if tipo == "sqlite":
        return f"sqlite:///{db}"
    if tipo == "sqlserver":
        return f"mssql+pyodbc://@{host}/{db}?driver=ODBC+Driver+17+for+SQL+Server&trusted_connection=yes"
    if tipo == "postgres":
        user_encoded = quote_plus(user)
        pwd_encoded = quote_plus(pwd)
        return f"postgresql+psycopg2://{user_encoded}:{pwd_encoded}@{host}:{port}/{db}"
    if tipo == "mysql":
        user_encoded = quote_plus(user)
        pwd_encoded = quote_plus(pwd)
        return f"mysql+pymysql://{user_encoded}:{pwd_encoded}@{host}:{port}/{db}"

@pytest.mark.parametrize("motor", motores)
def test_conexion_motor(motor):
    print(f"\n🔍 Probando conexión con: {motor.upper()}")
    try:
        v = valores_por_defecto[motor]
        url = construir_url(motor, v["usuario"], v["clave"], v["host"], v["puerto"], v["nombre_bd"])
        engine = create_engine(url)
        inspector = inspect(engine)
        tablas = inspector.get_table_names()
        print(f"✅ Conexión exitosa con {motor.upper()}. Tablas detectadas: {tablas}")
        assert True
    except OperationalError as e:
        print(f"⚠️ Error de conexión con {motor.upper()}: {e}")
        assert False, f"No se pudo conectar al motor {motor.upper()}"
    except Exception as e:
        print(f"❌ Excepción inesperada con {motor.upper()}: {e}")
        assert False, f"Error inesperado con motor {motor.upper()}"
