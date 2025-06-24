import pytest
import pandas as pd
from sqlalchemy import create_engine, text, inspect

@pytest.fixture
def motor_sqlite():
    engine = create_engine("sqlite:///:memory:")
    with engine.begin() as conn:
        conn.execute(text("""
            CREATE TABLE clientes (
                id_cliente INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                correo TEXT UNIQUE NOT NULL,
                ciudad TEXT NOT NULL
            );
        """))
    return engine

def test_insercion_exitosa(motor_sqlite):
    df = pd.DataFrame([
        {"nombre": "Mario", "correo": "mario@correo.com", "ciudad": "Lima"},
        {"nombre": "Lucia", "correo": "lucia@correo.com", "ciudad": "Arequipa"}
    ])

    df.to_sql("clientes", motor_sqlite, if_exists="append", index=False)
    resultado = pd.read_sql("SELECT * FROM clientes", motor_sqlite)

    assert resultado.shape[0] == 2
    assert "Mario" in resultado["nombre"].values

def test_insercion_con_valor_nulo(motor_sqlite):
    df = pd.DataFrame([
        {"nombre": None, "correo": "test@correo.com", "ciudad": "Lima"}  # nombre es NOT NULL
    ])

    with pytest.raises(Exception):
        df.to_sql("clientes", motor_sqlite, if_exists="append", index=False)

def test_insercion_duplicada_unique(motor_sqlite):
    df = pd.DataFrame([
        {"nombre": "Ana", "correo": "ana@correo.com", "ciudad": "Cusco"},
        {"nombre": "Ana2", "correo": "ana@correo.com", "ciudad": "Piura"}  # correo duplicado
    ])

    df.iloc[:1].to_sql("clientes", motor_sqlite, if_exists="append", index=False)
    with pytest.raises(Exception):
        df.iloc[1:].to_sql("clientes", motor_sqlite, if_exists="append", index=False)
